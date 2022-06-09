<template>
    <div id="myStore">
        <h3><input class="editBox" type="text" placeholder="Store Name" v-model="storeName"></h3>
        <h5><input class="editBox" type="text" placeholder="Address Number" v-model="storeAddress"></h5>
        <h5><input type="tel" placeholder="Phone Number" v-model="storePhone"></h5>
        <table>
            <thead>
                <th style="width:15%"></th>
                <th style="width:60%"></th>
                <th style="width:15%">
                    <template v-for="n in storeRating" :key="n">
                        <span class="fa fa-star checked"></span>
                    </template>
                    <template v-for="n in 5 - storeRating" :key="n">
                        <span class="fa fa-star"></span>
                    </template>
                </th>
            </thead>
        </table>


        <table>
            <thead>
                <th>Item</th>
                <th>Price</th>
                <th>Sales</th>
            </thead>
            <tbody>
                <tr v-for="(item,index) in storeItems" :key="item.id">
                    <td style="width:40%"><input type="text" placeholder="Item Name" v-model="item.name"> </td>
                    <td style="width:25%"><input type="number" min="0" oninput="validity.valid||(value='');" placerholder="Item Price" v-model="item.price"></td>
                    <td style="width:15%">{{item.sales}}</td>
                    <td style="width:15%">
                        <span @click="delItem(index)" id="trashBtn"><i class="fa fa-trash" style="color:red"/></span>
                    </td>
                </tr>
                <tr>
                    <td style="width:40%"></td>
                    <td style="width:25%"><button @click="addNew()" class="mt-1 btn btn-primary btn-block">Add New</button></td>
                    <td style="width:35%"></td>
                </tr>
            </tbody>
        </table>
        <button class="mt-1 btn btn-danger btn-block savebtn" @click="saveChange()">Save Changes</button>
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
            itemIDcounter : 1,
		};
	},
	methods: {
        addNew() {
            this.storeItems.push({
                id : this.itemIDcounter,
                name : "",
                price : 0,
                sales : 0
            });
            this.itemIDcounter++;
        },
        delItem(index) {
            this.storeItems.splice(index, 1);
        },
        async saveChange() {
            for(let i = 0; i < this.storeItems.length; i++) {
                if(this.storeItems[i].name == "") {
                    this.storeItems.splice(i, 1);
                    i--;
                }
            }
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
        this.storeItems = [ 
           {id:1, name:"Striver Food",price:32,sales:87},
           {id:2, name:"Striver Combo",price:100,sales:0},
        ]
	},
    beforeUnmount() {
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
.savebtn {
    width : 20%;
    float : right;
}
.editBox {
    width : 100%;
}
</style>
