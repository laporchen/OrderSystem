<template>
	<div id="app">
		<Nav />

		<div class="wrapper">
			<div class="inner">
				<router-view />
			</div>
		</div>
	</div>
</template>

<script>
import Nav from "./components/Nav.vue";
import axios from "axios";
export default {
	name: "App",
	components: {
		Nav,
	},
	async created() {
		const response = await axios.get("user").catch(() => {
			this.$router.push("/login");
		});
		if (response?.data?.status !== "success") {
			this.$router.push("/login");
		} else {
			await this.$store.dispatch("user", response?.data);
			this.$router.push("/browse");
		}
	},
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;500;600;700&display=swap");
* {
	font: sans-serif;
	box-sizing: border-box;
}
body {
	background-color: #afafaf;
	min-height: 100vh;
	display: flex;
}
nav {
	background-color: #f3f3f3;
}
body,
html,
#app,
#root,
.wrapper {
	width: 100%;
	height: 100%;
}
#app {
	text-align: center;
}
.wrapper {
	display: flex;
	justify-content: center;
	flex-direction: column;
	text-align: left;
}
.inner {
	max-height: 80%;
	width: 1000px;
	margin: auto;
	background-color: #fff;
	box-shadow: 0px 14px 80px #ccc rgba(0, 0, 0, 0.5);
	padding: 20px;
	border-radius: 20px;
	overflow: auto;
}

.inner > * {
	margin :30px;
}
.wrapper .form-control:focus {
	box-shadow: none;
}
.wrapper h3 {
	text-align: center;
	margin: 0;
	line-height: 1;
	padding-bottom: 20px;
}
.custom-control-label::before {
	font-weight: 400;
}
.checked {
    color: gold; 
}
.fav {
    color: pink;
}
</style>

