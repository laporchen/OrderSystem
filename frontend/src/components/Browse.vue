<template>
    <div id="browse" v-if="dataFetched">
        <div style="text-align:center; padding-bottom:30px"><h2>Browse the food you like.</h2></div>
        <table style="font-size:120%">
            <th style="width:5%">
                <p @click="favOnly = !favOnly" :class="{fav:favOnly}"><i  class="fa fa-solid fa-heart"></i></p>
            </th>
            <th style="width:40%">
                <input type="text" placeholder="Search" v-model="searchWord">
            </th>
            <th style="width:35%">
                <input v-model="minPrice" ype=number placeholder="Min" style="width:50%">
                <input v-model="maxPrice" type=number placeholder="Max" style="width:50%">
            </th>
            <th style="width:20%" class="ratingFilter">
                <span @click="minRating = 1"  :class="1 <= minRating ? 'checked' : ''"><i class="fa fa-star"/></span>
                <span @click="minRating = 2"  :class="2 <= minRating ? 'checked' : ''"><i class="fa fa-star"/></span>
                <span @click="minRating = 3"  :class="3 <= minRating ? 'checked' : ''"><i class="fa fa-star"/></span>
                <span @click="minRating = 4"  :class="4 <= minRating ? 'checked' : ''"><i class="fa fa-star"/></span>
                <span @click="minRating = 5"  :class="5 <= minRating ? 'checked' : ''"><i class="fa fa-star"/></span>
            </th>
        </table>
        <hr>
        <template v-for="store in stores" :key="store.storeID">
            <template v-if="filter(store.storeID)">
                <table style="font-size:120% " @click="gotoStore(store.storeID)">
                    <tbody>
                        <tr>
                            <td style="width:5%">
                                <i :class="{fav : userFav(store.storeID)} " class="fa fa-solid fa-heart" style="text-align:right"></i>
                            </td>
                            <td style="width:40%"><b>{{store.name}}</b></td>
                            <td style="width:35%">{{store.priceRange[0]}}$ ~ {{store.priceRange[1]}}$</td>
                            <td style="width:20%">
                                <template v-for="n in store.rating" :key="n">
                                    <i class="fa fa-star checked"></i>
                                </template>
                                <template v-for="n in 5- store.rating" :key="n">
                                    <i class="fa fa-star"></i>
                                </template>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <hr>
            </template>
        </template> 
    </div>
</template>


<script>
//import { mapGetters } from "vuex";
import axios from "axios";
export default {
	name: "Browse",
	data() {
		return {
            stores: [],
            maxPrice: 0,
            minPrice: 0,
            minRating:2,
            fav : [],
            searchWord: "",
            favOnly : false,
            dataFetched : false,
		};
	},
	methods: {
        filter(storeID) {
            // something that check the filter rule
            let store = this.stores.filter(obj =>{
                return obj.storeID == storeID;
            })
            if(store.length < 1 ) return false;
            store = store[0];
            let storeName = store.name.toLowerCase();
            return  store.priceRange[0] >= this.minPrice && 
                    ( store.priceRange[1] <= this.maxPrice || this.maxPrice == 0)&& 
                    store.rating >= this.minRating && 
                    storeName.includes(this.searchWord.toLowerCase()) &&
                    (this.favOnly === false || this.userFav(storeID));
        },
        gotoStore(storeID) {
			this.$router.push("/store/" + storeID);
        },
        userFav(storeID) {
            //something that check the store is in user's favorite
            return this.fav.includes(storeID);
        },
        updateRating(val) {
            this.minRating = val;
        },
        checkRating(val) {
            return this.minRating >= val;
        }
	},
	async created() {
        // fetching data here.
        let filter = {}; // filter rule
        let res = await axios.post("/getStores",{
            "filter" : filter,
            "userID" : this.$store.getters.user.user,
        });
        if(res?.data?.status !== "success") {
            this.$router.push("/404");
        }
        this.stores = res.data.stores;
        this.fav = res.data.fav;
        this.dataFetched = true;
	},
};
</script>

<style scoped>

table {
    width : 100%;
}
td ,th{
    width : 33%;
}

tr:hover {
    cursor:pointer;
    background-color:lightgrey;
}

.ratingFilter:hover {
    cursor:pointer;
}

</style>