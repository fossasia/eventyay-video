<template lang="pug">
.c-admin
	h1 admin
	p here be global config
</template>
<script>
export default {
	components: {},
	data () {
		return {
		}
	},
	computed: {},
	created () {},
	mounted () {
		this.$nextTick(() => {
		})
	},
	methods: {}
}
</script>
<style lang="stylus">
.c-admin
	padding: 0 16px

#app:not(.override-sidebar-close)  .c-admin
	+above('l')
		grid-area: app-bar;
		margin-left: var(--sidebar-width);
</style>
