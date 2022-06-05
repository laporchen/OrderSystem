<template>
    <div id="browse">
        <template v-for="store in stores" :key="store">
            <template v-if="filter(store.storeID)" >
                <table style="font-size:120% " @click="gotoStore(store.storeID)">
                    <tbody>
                        <tr>
                            <td style="width:40% "><b>{{store.name}}</b></td>
                            <td style="width:35%">Price Range : {{store.priceRange[0]}} - {{store.priceRange[1]}}</td>
                            <td style="width:25%">Rating {{store.rate}}</td>
                        </tr>
                    </tbody>
                </table>
                <br>
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
            stores: [] 
		};
	},
	methods: {
        filter(storeID) {
            // something that check the filter rule
            return storeID == storeID;
        },
        gotoStore(storeID) {
			this.$router.push("/store/" + storeID);
        }
	},
	created() {
        // fetching data here.
        this.stores = [
            {storeID:1,name:"Raj's Fast Food", address:"Striver Road 69",phone:"123456789",openTime:[["1000","1300"],["1900","0100"]],priceRange:[95,125],rate:4.5},
            {storeID:2,name:"Corgi's Fist", address:"NTNU Rooftop",phone:"77777777",openTime:[["0100","2300"]],priceRange:["295","1225"],rate:5},
        ]
	},
};
</script>

<style scoped>

table  {
  border: 1px solid;
}
table {
    width : 100%;
}
td ,th{
    width : 33%;
}

</style>