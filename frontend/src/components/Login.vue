<template>
	<div id="login">
		<form @submit.prevent="handleLogin">
			<h3>Login</h3>
			<div class="form-group">
				<label>Username</label>
				<input
					type="username"
					class="form-control"
					v-model="username"
					placeholder="Enter username"
				/>
			</div>
			<div class="form-group">
				<label>Password</label>
				<input
					type="password"
					class="form-control"
					v-model="password"
					placeholder="Enter password"
				/>
			</div>
			<button class="mt-1 btn btn-primary btn-block">Login</button>
		</form>
	</div>
</template>

<script>
import axios from "axios";
export default {
	name: "Login",
	data() {
		return {
			username: "",
			password: "",
			user: {
				username: "",
				password: "",
			},
		};
	},
	methods: {
		async handleLogin() {
			const loginUser = {
				username: this.username,
				password: this.password,
			};
			const response = await axios.post("login", loginUser);
			if (response?.data?.status !== "success") {
				alert("username or password is incorrect");
				return;
			} else {
				await localStorage.setItem("token", response.data.token);
				await this.$store.dispatch("user", response.data);
				await this.$store.dispatch("seller", response.data.isSeller);
				if(response.data.isSeller) {
					this.$router.push("/myStore");
				}
				else {
					this.$router.push("/browse");
				}
			}
		},
	},
};
</script>
