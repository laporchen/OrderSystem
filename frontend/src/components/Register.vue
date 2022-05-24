<template>
	<div id="register">
		<form @submit.prevent="handleSubmit">
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
				<label>Phone Number</label>
				<input
					type="tel"
					class="form-control"
					v-model="phoneNumber"
					placeholder="Enter phone number"
				/>
			</div>
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
			email: "",
			phoneNumber: "",
			password: "",
			password_confirmation: "",
			isSeller: false,
			user: {
				first_name: "",
				last_name: "",
				email: "",
				password: "",
				password_confirmation: "",
			},
		};
	},
	methods: {
		async handleSubmit(e) {
			e.preventDefault();
			const newUser = {
				first_name: this.first_name,
				last_name: this.last_name,
				email: this.email,
				password: this.password,
				tasks: [],
			};
			if (newUser.password !== this.password_confirmation) {
				alert("Passwords do not match");
				return;
			}
			let response = await axios.post("register", newUser);
			if (response?.data?.status !== "success") {
				console.log(response);
			} else {
				this.$router.push("/login");
			}
		},
	},
};
</script>
