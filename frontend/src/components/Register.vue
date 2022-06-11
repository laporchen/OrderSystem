<template>
	<div id="register">
		<form @submit.prevent="handleSubmit" >
			<h3>Register</h3>
			<div class="form-group">
				<label>First Name</label>
				<input
					type="text"
					class="form-control"
					v-model="first_name"
					placeholder="Enter first name"
				/>
			</div>
			<div class="form-group">
				<label>Last Name</label>
				<input
					type="text"
					class="form-control"
					v-model="last_name"
					placeholder="Enter last name"
				/>
			</div>
			<div class="form-group">
				<label>Username</label>
				<input
					type="tel"
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
			<div class="form-group">
				<label>Confirm password</label>
				<input
					type="password"
					class="form-control"
					v-model="password_confirmation"
					placeholder="Enter password"
				/>
			</div>
			<div class="form-group">
				<input
					type="checkbox"
					v-model="isSeller"
					value="isSeller"
					id="checkbox"
				/>
				<label for="checkbox">Sign up as a seller?</label> <br>
				<button class="mt-1 btn btn-primary btn-block">Sign up</button>
			</div>
		</form>
	</div>
</template>

<script>
import axios from "axios";
export default {
	name: "Register",
	data() {
		return {
			first_name: "",
			last_name: "",
			username: "",
			password: "",
			password_confirmation: "",
			isSeller: false,
		};
	},
	methods: {
		async handleSubmit(e) {
			e.preventDefault();
			const newUser = {
				username: this.username,
				first_name: this.first_name,
				last_name: this.last_name,
				password: this.password,
				isSeller: this.isSeller
			};
			if (newUser.password !== this.password_confirmation) {
				alert("Passwords do not match");
				return;
			}
			let response = await axios.post("register", newUser);
			if (response?.data?.status !== "success") {
				alert("Register failed!")
			} else {
				alert("Register successed!")
				this.$router.push("/login");
			}
		},
	},
};
</script>
