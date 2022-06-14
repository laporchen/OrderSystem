<template>
    <div id="myOrders">
        <div style="text-align:center; padding-bottom:30px"><h2>Orders</h2></div>
        <ul>
        <template v-for="(order,index) in orders" :key="order.orderNumber">
        <li>        
                <p>Order Date : {{order.orderDate}}</p>
                <b>User : {{order.user}}</b><br>
                <b :class="{ COMPLETED: 'completed', CANCELED: 'canceled', PREPARING: 'preparing', PENDING: 'pending' }[order.status]">
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
        <template v-if="order.status === 'PENDING'">
            <button class="btn btn-primary orderBtn" @click="changeOrderState(index,order.orderNumber,'PREPARING')">Confirm</button>
            <button class="btn btn-danger orderBtn" @click="changeOrderState(index,order.orderNumber,'CANCELED')">Reject</button>
        </template>
        <template v-else-if="order.status === 'PREPARING'">
            <button class="btn btn-success orderBtn" @click="changeOrderState(index,order.orderNumber,'COMPLETED')">Complete</button>
        </template>
        <b>Total : {{order.total}} </b>
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
        async changeOrderState(index,orderID,status) {
            let res = await axios.post("/updateStoreOrder",{
                userID : this.$store.state.user.user,
                isSeller : this.$store.state.seller,
                orderID : orderID,
                newStatus : status
            });
            if(res.data?.status !== "success") {
                alert("Error");
                return;
            }
            this.orders[index].status = status;
        },
	},
	async created() {
        // something to fetch user order data from backend.
        let response = await axios.post("/getStoreOrders",{
            userID : this.$store.state.user.user,
            isSeller : this.$store.state.seller
        });
        if(response?.data?.status === "success") {
            console.log(response.data.orders);
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
