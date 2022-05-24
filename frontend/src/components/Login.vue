<template>
	<div id="login">
		<form @submit.prevent="handleLogin">
			<h3>Login</h3>
			<div class="form-group">
				<label>Email</label>
				<input
					type="email"
					class="form-control"
					v-model="email"
					placeholder="Enter email"
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
			email: "",
			password: "",
			user: {
				email: "",
				password: "",
			},
		};
	},
	methods: {
		async handleLogin() {
			const loginUser = {
				email: this.email,
				password: this.password,
			};
			const response = await axios.post("login", loginUser);
			if (response?.data?.status !== "success") {
				alert("Email or password is incorrect");
				return;
			} else {
				await localStorage.setItem("token", response.data.token);
				await this.$store.dispatch("user", response.data);
				await this.$store.dispatch("todoList", response.data.tasks);
				this.$router.push("/home");
			}
		},
	},
};
</script>
