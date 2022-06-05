<template>
    <div id="favorite">
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

table, th, td {
}
table {
    width : 100%;
}
td ,th{
    width : 33%;
}

.checked {
    color: gold;
}
.fav {
    color: pink;
}
</style>
