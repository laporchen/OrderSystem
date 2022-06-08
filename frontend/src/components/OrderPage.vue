<template>
    <div id="orders">
        <div style="text-align:center; padding-bottom:30px"><h2>Your Orders</h2></div>
        <ul>
        <template v-for="order in orders" :key="order.orderNumber">
        <li>        
                <p>Order Date : {{order.orderDate}}</p>
                <b @click="gotoStore(order.storeID)" style="cursor:pointer">Store : {{order.store}}</b><br>
                <b :class="{ Complete: 'completed', Canceled: 'canceled', Preparing: 'preparing' }[order.status]">
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
export default {
	name: "OrderPage",
	data() {
		return {
            orders : [
                {orderNumber:1,orderDate:"2022/05/19",store:"Striver Pizza",storeID:1,orderItems : [{id: 32,name:"Striver Special",quantity : 1, price :100}, {id : 31,name:"Raj Cola", quantity: 69,price:690}],time:"2022-06-04 13:32",status : "Complete"},
                {orderNumber:2,orderDate:"2022/05/22",store:"Demon Burger", storeID:3,orderItems : [{id:2,name:"Corgi Special",quantity : 3,price:420},],time:"2022-06-05 20:32",status : "Canceled"},
                {orderNumber:3,orderDate:"2022/05/22",store:"Demon Burger", storeID:3,orderItems : [{id:2,name:"Corgi Special",quantity : 3,price:420},],time:"2022-06-05 20:32",status : "Canceled"},
                {orderNumber:4,orderDate:"2022/05/22",store:"Demon Burger", storeID:3,orderItems : [{id:2,name:"Corgi Special",quantity : 3,price:420},],time:"2022-06-05 20:32",status : "Canceled"},
                {orderNumber:5,orderDate:"2022/05/22",store:"Demon Burger", storeID:3,orderItems : [{id:2,name:"Corgi Special",quantity : 3,price:420},],time:"2022-06-05 20:32",status : "Canceled"},
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
        }
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
