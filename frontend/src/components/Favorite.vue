<template>
    <div id="favorite">
        <div style="text-align:center; padding-bottom:30px"><h2>Favorite Stores</h2></div>
        <template v-for="store in favoriteStores" :key="store"> 
            <table style="font-size:120% " @click="gotoStore(store.storeID)">
                <tbody>
                    <tr>
                        <td style="width:5% ">
                            <i class="fa fa-solid fa-heart fav" style="text-align:right"></i>
                        </td>
                        <td style="width:40% "><b>{{store.name}}</b></td>
                        <td style="width:35%">{{store.priceRange[0]}}$ ~ {{store.priceRange[1]}}$</td>
                        <td style="width:20%">
                            <template v-for="n in store.rate" :key="n">
                                <i class="fa fa-star checked"></i>
                            </template>
                            <template v-for="n in 5- store.rate" :key="n">
                                <i class="fa fa-star"></i>
                            </template>
                            </td>
                    </tr>
                </tbody>
            </table>
            <hr>
        </template>
    </div>
</template>

<script>
//import { mapGetters } from "vuex";
export default {
	name: "Store",
    data() {
		return {
            favoriteStores : [],
		};
	},
	methods: {
        gotoStore(storeID) {
			this.$router.push("/store/" + storeID);
        },
	},
	created() {
        // fetching store data here.
        //feteched data is assigned to the page here
        this.favoriteStores = [
            {storeID:2,name:"Corgi's Fist", address:"NTNU Rooftop",phone:"77777777",openTime:[["0100","2300"]],priceRange:["295","1225"],rate:5}
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
