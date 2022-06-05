<template>
    <div id="orders">
        <ul>
        <template v-for="order in orders" :key="order.orderNumber">
        <li>        
                <p>Order Number : {{order.orderNumber}}</p>
                <p>Store : {{order.store}}</p>
                <p>Order Status : {{order.status}}</p>
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
            orders : {
                1:{store:"Striver Pizza", orderItems : [{id: 32,name:"Striver Special",quantity : 1, price :100}, {id : 31,name:"Raj Cola", quantity: 69,price:690}],time:"2022-06-04 13:32",status : "Complete"},
                2:{store:"Demon Burger", orderItems : [{id:2,name:"Corgi Special",quantity : 3,price:420},],time:"2022-06-05 20:32",status : "Canceled"} 
            }
		};
	},
	methods: {
	},
	created() {
        // something to fetch user order data from backend.
	},
};
</script>

<style scoped>

table, th, td {
  border: 1px solid;
}
table {
    width : 100%;
}
td ,th{
    width : 33%;
}

</style>
