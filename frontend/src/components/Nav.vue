<template>
	<div id="nav">
		<nav class="navbar navbar-expand navbar-light fixed-top">
			<div class="container">
				<router-link class="navbar-brand" to="/">Striver Eats</router-link>
				<div class="collapse navbar-collapse">
					<ul v-if="!user" class="navbar-nav ms-auto">
						<li class="nav-item">
							<router-link to="/login" class="nav-link">Login</router-link>
						</li>
						<li class="nav-item">
							<router-link to="/register" class="nav-link"
								>Register</router-link
							>
						</li>
					</ul>
					<ul v-if="!user" class="navbar-nav ms-auto">
						<li class="nav-item">
							<router-link
								to="/browse"
								class="nav-link"
							>Browse</router-link>
						</li>
						<li class="nav-item">
							<router-link
								to="/cart"
								class="nav-link"
							>Shopping Cart</router-link>
						</li>
						<li class="nav-item">
							<router-link
								to="/orders"
								class="nav-link"
							>Orders</router-link>
						</li>
						<li class="nav-item">
							<router-link
								to="/favorite"
								class="nav-link"
							>My Favorite</router-link>
						</li>
						<li class="nav-item">
							<router-link
								to="/setting"
								class="nav-link"
							>Setting</router-link>
						</li>
						<li class="nav-item">
							<router-link
								to="/login"
								class="nav-link"
								@click="logoutHandle"
								>Logout</router-link
							>
						</li>
					</ul>
				</div>
			</div>
		</nav>
	</div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
	name: "Nav",
	methods: {
		logoutHandle() {
			localStorage.removeItem("token");
			this.$store.dispatch("user", null);
			this.$router.push("/login");
		},
	},
	computed: {
		...mapGetters(["user"]),
	},
};
</script>
