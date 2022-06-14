<template>
    <div id="cart">
        <!-- something like the browse page, but only show stores that user has non empty cart, and also show the total --> 
        <div style="text-align:center; padding-bottom:30px"><h2>Your Carts</h2></div>
        <div v-if="storeWithCart.length == 0">
            <h3>Nothing in your cart, go buy something</h3>
        </div>
        <template v-for="store in storeWithCart" :key="store"> 
            <table style="font-size:120% " @click="gotoStore(store.storeID)">
                <tbody>
                    <tr> 
                        <td style="width:45%"><b>{{store.name}}</b></td>
                        <td style="width:35%">{{store.itemCount}} items</td>
                        <td style="width:20%">{{store.totalPrice}}$</td>
                    </tr>
                </tbody>
            </table>
            <hr>
        </template>
    </div>
</template>


<script> 
import axios from "axios";
export default {
	name: "Store",
	data() {
		return {
            storeWithCart: [],
		};
	},
	methods: {
        gotoStore(storeID) {
			this.$router.push("/store/" + storeID);
        },
	},
	async created() {
        // fetching store data here.
        let res = await axios.post("/getCarts", {
            "userID" : this.$store.getters.user.user,
            "isSeller" : this.$store.getters.seller,
        })
        //feteched data is assigned to the page here
        if(res.data?.status === "success"){
            this.storeWithCart = res.data.carts;
        }
    }
};
</script>

<style scoped>
table ,tr ,th {
    width: 100%;
}

tr:hover {
    cursor:pointer;
    background-color:lightgrey;
}
</style>