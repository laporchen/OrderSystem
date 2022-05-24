<template>
	<div id="home">
		<h3 v-if="user">Welcome home, {{ user?.name }}</h3>
		<h3 v-else>You are not login</h3>
	</div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
	name: "Home",
	computed: {
		...mapGetters(["user"]),
	},
};
</script>
