<template>
	<div id="todo">
		<form @submit.prevent="handleSubmitNewTask">
			<h2 v-if="!submitValid" style="color: red">{{ invalidError }}</h2>
			<table class="table table-bordered mt-1 table">
				<thead>
					<tr>
						<th scope="col" style="width: 30%">Task</th>
						<th scope="col" style="width: 60%">Description</th>
						<th scope="col" style="width: 5%"></th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="(task, index) in getterTodoList" :key="index">
						<th>
							<span
								@click="taskMarkOff(index)"
								:class="{ taskDone: task.done }"
								>{{ task.name }}</span
							>
						</th>
						<th>
							<div @click="editDescription(index)">
								<span>{{ task.description }}&nbsp;</span>
							</div>
						</th>
						<th @click="deleteTask(index)">
							<div>
								<span class="fa fa-trash"></span>
							</div>
						</th>
					</tr>
					<tr>
						<th>
							<input
								type="text"
								class="form-control"
								v-model="inputTask.name"
								placeholder="Enter task name"
								required
							/>
						</th>
						<th>
							<input
								type="text"
								class="form-control"
								v-model="inputTask.description"
								placeholder="Enter task description"
							/>
						</th>
					</tr>
				</tbody>
			</table>
			<button class="mt-1 btn btn-primary btn-block">Submit</button>
		</form>
	</div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
	name: "TodoList",
	data() {
		return {
			inputTask: {
				name: "",
				description: "",
				done: false,
			},
			todoListData: [],
			submitValid: true,
			invalidError: "",
		};
	},
	methods: {
		async handleSubmitNewTask() {
			const exist = this.todoListData?.find(
				(task) => task.name === this.inputTask.name
			);
			if (exist) {
				this.invalidError = "Task already exist";
				this.submitValid = false;
				return;
			}
			this.submitValid = true;
			this.todoListData.push(JSON.parse(JSON.stringify(this.inputTask)));
			this.$store.dispatch("updateTodoList", this.todoListData);
		},
		taskMarkOff(index) {
			this.todoListData[index].done = !this.todoListData[index].done;
			this.$store.dispatch("updateTodoList", this.todoListData);
		},
		editDescription(index) {
			let newDesc = prompt(
				"Enter new description",
				this.todoListData[index].description
			);
			if (newDesc === null) return;
			this.todoListData[index].description = newDesc;
			this.$store.dispatch("updateTodoList", this.todoListData);
		},
		deleteTask(index) {
			this.todoListData.splice(index, 1);
			this.$store.dispatch("updateTodoList", this.todoListData);
		},
	},
	created() {
		this.todoListData = this.$store.getters.todoList;
	},
	computed: {
		...mapGetters({
			getterTodoList: "todoList",
		}),
	},
};
</script>

<style>
.taskDone {
	text-decoration: line-through;
}
table {
	empty-cells: show;
}
</style>
