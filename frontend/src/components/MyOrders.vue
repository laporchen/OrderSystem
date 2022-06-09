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
export default {
	name: "OrderPage",
	data() {
		return {
            orders : [
                {orderNumber:1,orderDate:"2022/05/19",user:"Striver",orderItems : [{id: 32,name:"Striver Special",quantity : 1}, {id : 31,name:"Raj Cola", quantity: 69}],time:"2022-06-04 13:32",status : "Pending"},
                {orderNumber:2,orderDate:"2022/05/19",user:"Raj",orderItems : [{id: 32,name:"Striver Special",quantity : 5}],time:"2022-06-04 13:32",status : "Completed"},
                {orderNumber:4,orderDate:"2022/05/19",user:"Ra",orderItems : [{id: 32,name:"Striver Special",quantity : 5}],time:"2022-06-04 13:32",status : "Pending"},
                {orderNumber:3,orderDate:"2022/05/19",user:"Rj",orderItems : [{id: 32,name:"Striver Special",quantity : 5}],time:"2022-06-04 13:32",status : "Preparing"},
            ]
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
            this.orders[index].status = "Completed";
            console.log(index,orderID);
        },
        async cancelOrder(index,orderID) {
            this.orders[index].status = "Canceled";
            console.log(index,orderID);
        },
        async confirmOrder(index,orderID) {
            this.orders[index].status = "Preparing";
            console.log(index,orderID);
        },
	},
	created() {
        // something to fetch user order data from backend.
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
