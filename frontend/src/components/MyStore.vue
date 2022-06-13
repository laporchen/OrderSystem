<template>
    <div id="myStore" v-if="dataFetched">
        <h3><input class="editBox" type="text" placeholder="Store Name" v-model="storeName"></h3>
        <div style="display:table">
            <div style="display:table-cell">
                <input class="editBox" type="text" placeholder="City" v-model="storeAddress.city">
            </div>
            <div style="display:table-cell">
                <input class="editBox" type="text" placeholder="District" v-model="storeAddress.district">
            </div>
            <div style="display:table-cell">
                <input class="editBox" type="text" placeholder="Road" v-model="storeAddress.road">
            </div>
            <div style="display:table-cell">
                <input class="editBox" type="text" placeholder="Lane" v-model="storeAddress.lane">
            </div>
            <div style="display:table-cell">
                <input class="editBox" type="text" placeholder="Alley" v-model="storeAddress.alley">
            </div>
            <div style="display:table-cell">
                <input class="editBox" type="number" placeholder="No" v-model="storeAddress.no">
            </div>
            <div style="display:table-cell">
                <label>號</label>
            </div>
            <div style="display:table-cell">
                <input class="editBox" type="number" placeholder="Floor" v-model="storeAddress.floor">
            </div>
            <div style="display:table-cell">
                <label>樓</label>
            </div>
        </div>
        <h5><input type="tel" placeholder="Phone Number" v-model="storePhone"></h5>
        <table>
            <thead>
                <th style="width:15%"></th>
                <th style="width:60%"></th>
                <th style="width:15%">
                    <template v-for="n in 5" :key="n">
                        <span :class="{checked:(n<=storeRating)}" class="fa fa-star"></span>
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
import axios from "axios";
export default {
	name: "Store",
	data() {
		return {
            storeName : null,
            storePhone : null,
            storeAddress : {
                city: "",
                district:"" ,
                road:"" ,
                lane:"" ,
                alley:"",
                no:"",
                floor:"",
            },
            storeRating : 0,
            storeItems : [],
            storeID : null,
            itemIDcounter : 1,
            oldItem : [],
            delItemID : [],
            modifyItem : [],
            newItem : [],
            dataFetched : false,
		};
	},
	methods: {
        addNew() {
            this.storeItems.push({
                id : this.IDcounter,
                name : "",
                price : 0,
                sales : 0
            });
            this.IDcounter++;
        },
        delItem(index) {
            this.storeItems.splice(index, 1);
        },
        async saveChange() {

            this.storeItems.forEach((item) => {
                let contain = this.oldItem.some((oldItem) => {
                    return oldItem.id == item.id;
                });
                let modify = this.oldItem.some((oldItem)=> {
                    return oldItem.id == item.id && (oldItem.name != item.name || oldItem.price != item.price);
                });
                if(!contain) {
                    this.newItem.push(item);
                }
                else if(modify) {
                    this.modifyItem.push(item);
                }
            })
            this.oldItem.forEach((item) => {
                let contain = this.storeItems.some((storeItem) => {
                    return storeItem.id == item.id;
                });
                if(!contain) {
                    this.delItemID.push(item.id);
                }
            })
            for(let i = 0; i < this.storeItems.length; i++) {
                if(this.storeItems[i].name == "") {
                    this.storeItems.splice(i, 1);
                    i--;
                }
            }

            // fire event to backend
            let response = await axios.post("/updateStore", {
                isSeller : this.$store.state.seller,
                userID : this.$store.getters.user,
                storeID : this.storeID,
                store : {
                    storeName : this.storeName,
                    storeAddress : this.storeAddress,
                    storePhone : this.storePhone,
                    newItem : this.newItem,
                    delItemID : this.delItemID,
                    modifyItem : this.modifyItem,
                }
            });       
            if(response?.data?.status != "success") {
                alert("Error : Cannot update your store, please try again later");
            }
            else {
                alert("Success : Your store has been updated");
                this.$router.go()
            }
            // if failed then give an error message to user
        }
	},
	async created() {
        // fetching store data here.
        // if store does not exist , redirect to home page
        //feteched data is assigned to the page here
        let response = await axios.post("/store", {
            isSeller : this.$store.state.seller,
            userID : this.$store.getters.user.user,
            storeID: 0,
        });
        if(response?.data?.status != "success") {
            this.$router.push("/");
        }
        let storeInfo = response.data.store;
        console.log(storeInfo)
        this.storeName = storeInfo.storeName;
        this.storeID = storeInfo.storeID;
        this.storePhone = storeInfo.storePhone;
        this.storeAddress = storeInfo.storeAddress;
        this.storeRating = storeInfo.storeRating;
        this.storeItems = storeInfo.storeItems;
        this.itemIDcounter = storeInfo.IDcounter;
        this.oldItem = JSON.parse(JSON.stringify(storeInfo.storeItems));
        this.dataFetched = true;
	},
    async beforeUnmount() {
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
