<template>
    <div id="store">
        <h3>{{storeName}}</h3>
        <h5>{{storeAddress}}</h5>
        <table>
            <thead>
                <th style="width:15%"><h4>{{storePhone}}</h4></th>
                <th style="width:60%"></th>
                <th style="width:15%">
                    <template v-for="n in storeRating" :key="n">
                        <span class="fa fa-star checked"></span>
                    </template>
                    <template v-for="n in 5 - storeRating" :key="n">
                        <span class="fa fa-star"></span>
                    </template>
                </th>
                <th style="width:10% font:120%" @click="userFav = !userFav" :class="{fav:userFav}"><span class="fa fa-heart"></span></th>
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
                        <td style="width:25%"><button class="mt-1 btn btn-danger btn-block" @click="sentOrder()">Place Order</button></td>
                    </tr>
                </tbody>
            </table>
        </template>
    </div>
</template>

<script>
//import { mapGetters } from "vuex";
export default {
	name: "Store",
	data() {
		return {
            storeName : null,
            storePhone : null,
            storeAddress : null,
            storeRating : 0,
            storeItems : [],
            storeID : null,
            currentTotal : 0,
            userFav : false,
            userCart : {},
            cartHasItem : false
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
            // if failed then give an error message to user
        }
	},
	created() {
        // fetching store data here.
        // if store does not exist , redirect to home page
        //feteched data is assigned to the page here
        this.storeName = "Raj's Fast Food";
        this.storeID = 1;
        this.storePhone = "093112651";
        this.storeAddress = "106台北市大安區和平東路一段162號";
        this.storeRating = 4;
        this.storeItems = { 
           1:{id:1, name:"Striver Food",price:32},
           2:{id:2, name:"Striver Combo",price:100},
        }
        // assigned users cart to useCart if it exists
        this.hasItem();
	},
    beforeUnmount() {
        // save user's cart to database
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
