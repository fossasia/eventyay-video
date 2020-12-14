<template lang="pug">
.c-question(:class="{queued: hasPermission('room:question.moderate') && question.state === 'mod_queue'}")
	.votes
		.mdi.mdi-menu-up.upvote
		.vote-count 0
		| Votes
	.content {{ question.content }}
	menu-dropdown(v-if="hasPermission('room:question.moderate')", v-model="modding")
		template(v-slot:button="{toggle}")
			bunt-icon-button(@click="toggle") dots-vertical
		template(v-slot:menu)
			.approve-question(@click="approveQuestion") {{ $t('Questions:asking-form:mod-approve-question:label') }}
			.delete-question(@click="deleteQuestion") {{ $t('Questions:asking-form:mod-delete-question:label') }}
</template>
<script>
import { mapGetters } from 'vuex'
import MenuDropdown from 'components/MenuDropdown'

export default {
	components: { MenuDropdown },
	props: {
		question: Object
	},
	data () {
		return {
			modding: false
		}
	},
	computed: {
		...mapGetters(['hasPermission'])
	},
	created () {},
	mounted () {
		this.$nextTick(() => {
		})
	},
	methods: {
		async approveQuestion () {
			await this.$store.dispatch('question/approveQuestion', this.question)
			this.modding = false
		},
		deleteQuestion () {

		}
	}
}
</script>
<style lang="stylus">
.c-question
	flex: none
	display: flex
	align-items: center
	border-bottom: border-separator()
	position: relative
	.votes
		display: flex
		flex-direction: column
		align-items: center
		margin: 8px
		color: $clr-secondary-text-light
		text-transform: uppercase
		font-size: 12px
		.mdi
			font-size: 38px
			line-height: 8px
		.vote-count
			font-family: 'Roboto-Condensed'
			font-weight: 200
			font-size: 32px
			line-height: 32px
			color: $clr-primary-text-light
			// TODO scaling for digits
	.content
		flex: auto
		margin: 8px
	&.queued
		$clr-queued = alpha($clr-black, .05)
		background: repeating-linear-gradient(-45deg, transparent, transparent 10px, $clr-queued 10px, $clr-queued 20px, transparent 20px)
		&::after
			content: 'needs approval'
			display: block
			position: absolute
			right: 8px
			top: 8px
			font-size: 12px
			color: $clr-deep-orange
			font-weight: 600
</style>