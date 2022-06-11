<template>
    <div id="myOrders">
        <div style="text-align:center; padding-bottom:30px"><h2>Orders</h2></div>
        <ul>
        <template v-for="(order,index) in orders" :key="order.orderNumber">
        <li>        
                <p>Order Date : {{order.orderDate}}</p>
                <b>User : {{order.user}}</b><br>
                <b :class="{ Completed: 'completed', Canceled: 'canceled', Preparing: 'preparing', Pending: 'pending' }[order.status]">
                            Order Status : {{order.status}}
                </b>

                <table>
                    <thead>
                        <th>Quantity</th>
                        <th>Name</th>
                    </thead>
                    <tbody v-for="item in order.orderItems" :key="item">
                        <tr>
                            <td>{{item.quantity}}</td>
                            <td>{{item.name}}</td>
                        </tr>
                    </tbody>
                </table>
        </li>        
        <template v-if="order.status === 'Pending'">
            <button class="btn btn-primary orderBtn" @click="confirmOrder(index,order.orderNumber)">Confirm</button>
            <button class="btn btn-danger orderBtn" @click="cancelOrder(index,order.orderNumber)">Reject</button>
        </template>
        <template v-else-if="order.status === 'Preparing'">
            <button class="btn btn-success orderBtn" @click="completeOrder(index,order.orderNumber)">Complete</button>
        </template>
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
        async completeOrder(index,orderID) {
            let res = await axios.post("/updateStoreOrder",{
                userID : this.$store.state.user,
                isSeller : this.$store.state.seller,
                orderID : orderID,
                newStatus : "Completed"
            });
            if(res.data?.status !== "success") {
                alert("Error");
                return;
            }
            this.orders[index].status = "Completed";
        },
        async cancelOrder(index,orderID) {
            let res = await axios.post("/updateStoreOrder",{
                userID : this.$store.state.user,
                isSeller : this.$store.state.seller,
                orderID : orderID,
                newStatus : "Canceled"
            });
            if(res.data?.status !== "success") {
                alert("Error");
                return;
            }
            this.orders[index].status = "Canceled";
        },
        async confirmOrder(index,orderID) {
            let res = await axios.post("/updateStoreOrder",{
                userID : this.$store.state.user,
                isSeller : this.$store.state.seller,
                orderID : orderID,
                newStatus : "Preparing"
            });
            if(res.data?.status !== "success") {
                alert("Error");
                return;
            }
            this.orders[index].status = "Preparing";
        },
	},
	async created() {
        // something to fetch user order data from backend.
        let response = await axios.post("/getStoreOrders",{
            userID : this.$store.state.user,
            isSeller : this.$store.state.seller
        });
        if(response?.data?.status === "success") {
            this.orders = response.data.orders;
        }
        else {
            this.$router.push("/");
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

.orderBtn{
    width:15%;
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
