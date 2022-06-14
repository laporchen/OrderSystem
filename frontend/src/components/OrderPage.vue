<template>
    <div id="orders">
        <div style="text-align:center; padding-bottom:30px"><h2>Your Orders</h2></div>
        <ul>
        <template v-for="(order,index) in orders" :key="order.orderNumber">
        <li>        
                <p>Order Time: {{order.time}}</p>
                <b @click="gotoStore(order.storeID)" style="cursor:pointer">Store : {{order.storeName}}</b>
                <div v-if="order.status === 'COMPLETED'">
                    <template v-if="order.rating === 0">
                        <b>Not rated : </b>
                        <template v-for="n in 5" :key="n">
                            <span @click="rateOrder(n,order.orderNumber,order.storeID,index)"><i class="fa fa-star "></i></span>
                        </template>
                    </template>
                    <template v-else>
                        <b>Rated : </b>
                        <span v-for="n in order.rating" :key="n"><i class="fa fa-star checked"></i></span>
                        <span v-for="n in 5 - order.rating" :key="n"><i class="fa fa-star"></i></span>
                    </template>
                </div>
                <br v-else>
                <b :class="{ COMPLETED: 'completed', CANCELED: 'canceled', PREPARING: 'preparing', PENDING: 'pending' }[order.status]">
                            Order Status : {{order.status}}
                </b>

                <table>
                    <thead>
                        <th>Quantity</th>
                        <th>Name</th>
                        <th>Subtotal</th>
                    </thead>
                    <tbody v-for="item in order.orderItems" :key="item">
                        <tr>
                            <td>{{item.quantity}}</td>
                            <td>{{item.name}}</td>
                            <td>{{item.price}}</td>
                        </tr>
                    </tbody>
                </table>
        </li>        
        <b>Total : {{sumPrice(order)}} </b>
        <hr>
        </template> 
        </ul>
    </div>
</template>

<script>
//import { mapGetters } from "vuex";
import axios from "axios";
export default {
	name: "OrderPage",
	data() {
		return {
            orders : []
		};
	},
	methods: {
        gotoStore(storeID) {
			this.$router.push("/store/" + storeID);
        },
        sumPrice(order) {
            let sum = 0;
            order.orderItems.forEach(item => sum += item.price);
            return sum;
        },
        async rateOrder(rating,orderNumber,storeID,index) {
            let res = await axios.post("/rateOrder", {
                "userID" : this.$store.getters.user.user,
                "isSeller" : this.$store.getters.seller,
                "storeID" : storeID,
                "orderID" : orderNumber,
                "rating" : rating,
            })
            if(res.data?.status === "success") {
                this.orders[index].rating = rating;
            }
            else {
                alert("Failed to rate this order.")
            }
            //fire an event to backend to update db
        }
	},
	async created() {
        // something to fetch user order data from backend.
        let res = await axios.post("/userOrders",{
            "userID" : this.$store.getters.user.user,
            "isSeller" : this.$store.getters.seller,
        })
        if(res.data?.status === "success") {
            this.orders = res.data.orders;
            console.log(res.data.orders)
        } 
	},
};
</script>

<style scoped>


.completed {
    color : green;
}

.canceled {
    color : red;
}

.preparing {
    color : orange;
}

.pending {
    color : blue;
}

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

</style>
