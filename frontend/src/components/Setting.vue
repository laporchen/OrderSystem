<template>
    <div id="setting">
        <div style="text-align:center; padding-bottom:30px"><h2>Setting</h2></div>
		<form @submit.prevent="handleSetting"> 
			<h3>Change Password</h3>
			<div class="form-group">
				<input
					type="password"
					class="form-control"
					v-model="oldPassword"
					placeholder="Enter old password"
				/>
			</div>
            <br>
			<div class="form-group">
				<input
					type="password"
					class="form-control"
					v-model="newPassword"
					placeholder="Enter new password"
				/>
			</div>
            <br>
			<div class="form-group">
				<input
					type="password"
					class="form-control"
					v-model="confirmPassword"
					placeholder="Confirm new password"
				/>
			</div>
			<button class="mt-1 btn btn-primary btn-block">Confirm</button>
		</form>
    </div>
</template>


<script>
import axios from "axios";
export default {
    name : "Setting",
    data() {
        return {
            oldPassword : "",
            newPassword : "",
            confirmPassword : "",
        }
    },
    methods : {
        async handleSetting() {
            if(this.newPassword != this.confirmPassword) {
                alert("New password and confirm password are not the same.");
                return;
            }
            let data = {
                username: this.$store.getters.user.user,
                oldPassword : this.oldPassword,
                newPassword : this.newPassword,
                confirmPassword : this.confirmPassword
            };
            let response = await axios.post("/changePassword", data);
            if(response.data.status === "success") {
                alert("Password changed successfully!");
            }
            else {
                alert("Password change failed!");
            }
        }   
    }
}

</script>