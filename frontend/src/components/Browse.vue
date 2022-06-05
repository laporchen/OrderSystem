<template>
    <div id="browse">
        <div style="text-align:center; padding-bottom:30px"><h2>Browse the food you like.</h2></div>
        <table>
            <th style="width:45%">Filter</th>
            <th style="width:35%"><input v-model="minPrice" type=number placeholder="Min" style="width:50%"><input v-model="maxPrice" type=number placeholder="Max" style="width:50%"></th>
            <th style="width:20% font-size:120%" hover="cursor:pointer">
                <input type=range min="0" max="5" v-model="minRating"> 
            </th>
        </table>
        <hr>
        <template v-for="store in stores" :key="store">
            <template v-if="filter(store.storeID)">
                <table style="font-size:120% " @click="gotoStore(store.storeID)">
                    <tbody>
                        <tr>
                            <td style="width:5% ">
                                <i :class="{fav : userFav(store.storeID)} " class="fa fa-solid fa-heart" style="text-align:right"></i>
                            </td>
                            <td style="width:40% "><b>{{store.name}}</b></td>
                            <td style="width:35%">{{store.priceRange[0]}}$ ~ {{store.priceRange[1]}}$</td>
                            <td style="width:20%">
                                <template v-for="n in store.rate" :key="n">
                                    <span class="fa fa-star checked"></span>
                                </template>
                                <template v-for="n in 5- store.rate" :key="n">
                                    <span class="fa fa-star"></span>
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
export default {
	name: "Browse",
	data() {
		return {
            stores: [],
            maxPrice: 9999,
            minPrice: 0,
            minRating:2
		};
	},
	methods: {
        filter(storeID) {
            // something that check the filter rule
            let store = this.stores.filter(obj =>{
                return obj.storeID == storeID;
            })
            
            if(store.length < 1) return false;
            store = store[0];
            return store.priceRange[0] >= this.minPrice && store.priceRange[1] <= this.maxPrice && store.rate >= this.minRating;
        },
        gotoStore(storeID) {
			this.$router.push("/store/" + storeID);
        },
        userFav(storeID) {
            //something that check the store is in user's favorite
            return storeID % 2 == 0;
        },
        updateRate(val) {
            this.minRating = val;
        },
        checkRate(val) {
            return this.minRating >= val;
        }
	},
	created() {
        // fetching data here.
        this.stores = [
            {storeID:1,name:"Raj's Fast Food", address:"Striver Road 69",phone:"123456789",openTime:[["1000","1300"],["1900","0100"]],priceRange:[95,125],rate:4},
            {storeID:2,name:"Corgi's Fist", address:"NTNU Rooftop",phone:"77777777",openTime:[["0100","2300"]],priceRange:[595,1225],rate:5},
            {storeID:3,name:"Corgi's Fist", address:"NTNU Rooftop",phone:"77777777",openTime:[["0100","2300"]],priceRange:[295,1225],rate:2},
            {storeID:4,name:"Corgi's Fist", address:"NTNU Rooftop",phone:"77777777",openTime:[["0100","2300"]],priceRange:[95,225],rate:3},
            {storeID:5,name:"Corgi's Fist", address:"NTNU Rooftop",phone:"77777777",openTime:[["0100","2300"]],priceRange:[5,12],rate:0},
            {storeID:6,name:"Corgi's Fist", address:"NTNU Rooftop",phone:"77777777",openTime:[["0100","2300"]],priceRange:[9,225],rate:1},
            {storeID:7,name:"Corgi's Fist", address:"NTNU Rooftop",phone:"77777777",openTime:[["0100","2300"]],priceRange:[29,1225],rate:4},
            {storeID:8,name:"Corgi's Fist", address:"NTNU Rooftop",phone:"77777777",openTime:[["0100","2300"]],priceRange:[29,122],rate:3},
            {storeID:9,name:"Corgi's Fist", address:"NTNU Rooftop",phone:"77777777",openTime:[["0100","2300"]],priceRange:[295,335],rate:3},
        ]
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

.checked {
    color: gold; 
}
.fav {
    color: pink;
}

</style>