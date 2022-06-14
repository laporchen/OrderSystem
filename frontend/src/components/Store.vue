<template>
    <div id="store" v-if="dataFetched">
        <h3>{{storeName}}</h3>
        <h5>Address : {{storeAddress}}</h5>
        <table>
            <thead>
                <th style="width:15%"><h4>{{storePhone}}</h4></th>
                <th style="width:60%"></th>
                <th style="width:15%">
                    <template v-for="n in 5" :key="n">
                        <span :class="{checked:(n<=storeRating)}" class="fa fa-star"></span>
                    </template>
                </th>
                <th style="width:10% font:120%" @click="favClick()" :class="{fav:userFav}"><span class="fa fa-heart"></span></th>
            </thead>
        </table>


        <table>
            <thead>
                <th>Item</th>
                <th>Price</th>
                <th></th>
            </thead>
            <tbody v-for="(item) in storeItems" :key="item.id">
                <tr>
                    <td style="width:50%">{{item.name}} </td>
                    <td style="width:25%">${{item.price}}</td>
                    <td style="width:25%"><button class="mt-1 btn btn-primary btn-block" @click="addCart(item.id)">Add One</button></td>
                </tr>
            </tbody>
        </table>
        <template v-if="cartHasItem">
            <br>
            <h4>Your Cart : </h4>
            <table>
                <thead>
                    <th>Item</th>
                    <th>Quantity</th>
                    <th></th>
                </thead>
                <tbody >
                    <template v-for="(item) in storeItems" :key="item.id">
                        <tr v-if="userCart[item.id] > 0">
                            <td style="width:50%">{{item.name}} </td>
                            <td style="width:25%">{{userCart[item.id]}}</td>
                            <td style="width:25%"><button class="mt-1 btn btn-primary btn-block" @click="delCart(item.id)">Remove One</button></td>
                        </tr>
                    </template>
                    <tr>
                        <td style="width:50%">Total : {{caculateTotal()}} </td>
                        <td style="width:25%"></td>
                        <td style="width:25%"><button class="mt-1 btn btn-danger btn-block" @click="placeOrder()">Place Order</button></td>
                    </tr>
                </tbody>
            </table>
        </template>
    </div>
</template>

<script>
//import { mapGetters } from "vuex";o
import axios from "axios"
export default {
	name: "Store",
	data() {
		return {
            storeName : null,
            storePhone : null,
            storeAddress : null,
            storeRating : 0,
            storeItems : {},
            storeID : null,
            currentTotal : 0,
            userFav : false,
            userCart : {},
            orderID : 0,
            cartHasItem : false,
            dataFetched : false,
		};
	},
	methods: {
        addCart(itemIndex){
            if(itemIndex in this.userCart) {
                this.userCart[itemIndex]+= 1;
            }
            else {
                this.userCart[itemIndex] = 1;
            }
            this.cartHasItem = true;
            return;
        },
        delCart(itemIndex) {
            if(itemIndex in this.userCart) {
                this.userCart[itemIndex]-= 1;
            }
            this.hasItem();
        },
        caculateTotal() {
            let sum = 0;
            for (const [key, value] of Object.entries(this.userCart)) {
                sum += this.storeItems[key].price * value;
            }
            return sum;
        },
        hasItem() {
            for (const obj of Object.entries(this.userCart)) {
                if(obj[1] != 0) {
                    this.cartHasItem = true;
                    return;
                }
            }
            this.cartHasItem = false;
        },
        async placeOrder() {
            // fire event to backend
            if(isNaN(this.orderID)) {
                this.orderID = -1;
            }
            let para = {
                "userID" : this.$store.getters.user.user,
                "isSeller" : this.$store.getters.seller,
                "storeID" : this.storeID,
                "orderID" : this.orderID,
                "cart" : this.userCart,
                "total" : this.caculateTotal()
            };
            console.log(para);
            let response = await axios.post("/placeOrder",para)
            if(response.data?.status === "success") {
                alert("Order placed.")
                this.$router.go();
            }
            else {
                alert("Order failed to place.")
            }
            // if failed then give an error message to user
        },
        async favClick() {
            let res = await axios.post("userFavStoreUpdate", {
                username : this.$store.getters.user.user,
                storeID : this.storeID,
            })
            if(res.data?.status === "success") {
                this.userFav = !this.userFav
            }
        }

	},
	async beforeCreate() {
        // fetching store data here.
        // if store does not exist , redirect to home page
        //feteched data is assigned to the page here
        let res = await axios.post("/store",{
            "username":this.$store.getters.user.user,
            "isSeller":this.$store.getters.seller,
            "storeID": this.$route.params.storeName
        })
        if(res.data?.status !== "success") {
            this.$router.push("/browse");
            return;
        }

        let s = res.data.store;
        this.storeName = s.storeName;
        this.storeID = s.storeID;
        this.storePhone = s.storePhone;
        this.storeAddress = s.storeAddress;
        this.storeRating = s.storeRating;
        this.orderID = s.orderID;
        s.storeItems.forEach((item) => {
            this.storeItems[item.id] = {
                "id": item.id,
                "name": item.name,
                "price": item.price
            };
        });
        this.userCart = res.data.cart;
        this.userFav = res.data.userFav;
        // assigned users cart to useCart if it exists
        console.log(this.userCart)
        this.hasItem();
        this.dataFetched = true;
	},
    async beforeUnmount() {
        // save user's cart to database
        await axios.post("/updateCart", {
            "userID" : this.$store.getters.user.user,
            "storeID" : this.storeID,
            "cart" : this.userCart,    
            "isSeller" : this.$store.getters.seller,
            "total" : this.caculateTotal(),
        })
    }
};
</script>

<style scoped>

table {
	border-collapse : collapse;
    width : 100%;
}
tr {
	border: solid;
	border-width : 1px 0;
}
td ,th{
    width : 33%;
}

button {
    width : 80%;
}

.checked {
    color: gold;
}
</style>
