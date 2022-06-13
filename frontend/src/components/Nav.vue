<template>
	<div id="nav">
		<nav class="navbar navbar-expand navbar-light fixed-top">
			<div class="container">
				<router-link class="navbar-brand" to="/">
					<img width="30" height="30" src="@/assets/raj.png">
					Striver Eats
				</router-link>
				<div class="collapse navbar-collapse">
					<template v-if="!user">
						<ul class="navbar-nav ms-auto">
							<li class="nav-item">
								<router-link to="/login" class="nav-link">Login</router-link>
							</li>
							<li class="nav-item">
								<router-link to="/register" class="nav-link"
									>Register</router-link
								>
							</li>
						</ul>
					</template>
					<template v-else>
						<ul class="navbar-nav ms-auto">
							<template v-if="!seller">
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
									>Cart</router-link>
								</li>
								<li class="nav-item">
									<router-link
										to="/orders"
										class="nav-link"
									>Orders</router-link>
								</li>
							</template>
							<template v-else>
								<li class="nav-item">
									<router-link
										to="/myStore"
										class="nav-link"
									>Store</router-link>
								</li>
								<li class="nav-item">
									<router-link
										to="/myOrders"
										class="nav-link"
									>Orders</router-link>
								</li>
							</template>
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
					</template>
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
		...mapGetters(["seller"]),
	},
	mounted() {
	}
};
</script>
