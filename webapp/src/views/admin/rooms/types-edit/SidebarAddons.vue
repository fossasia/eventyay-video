<template lang="pug">
.c-sidebar-addons
	h2 Sidebar addons
	bunt-switch(name="enable-chat", v-model="hasChat", label="Enable Chat")
	bunt-switch(name="enable-qa", v-model="hasQuestions", label="Enable Q&A")
	template(v-if="hasQuestions")
		bunt-checkbox(v-model="modules['question'].config.active", label="Active", name="active")
		bunt-checkbox(v-model="modules['question'].config.requires_moderation", label="Questions require moderation", name="requires_moderation")
	bunt-switch(v-if="$features.enabled('polls')", name="enable-polls", v-model="hasPolls", label="Enable Polls")
</template>
<script>
import mixin from './mixin'

export default {
	mixins: [mixin],
	data() {
		return {
		}
	},
	computed: {
		hasChat: {
			get() {
				return !!this.modules['chat.native']
			},
			set(value) {
				if (value) {
					this.addModule('chat.native', {volatile: true})
				} else {
					this.removeModule('chat.native')
				}
			}
		},
		hasQuestions: {
			get() {
				return !!this.modules.question
			},
			set(value) {
				if (value) {
					this.addModule('question', {
						active: true,
						requires_moderation: false
					})
				} else {
					this.removeModule('question')
				}
			}
		},
		hasPolls: {
			get() {
				return !!this.modules.poll
			},
			set(value) {
				if (value) {
					this.addModule('poll', {
						active: true
					})
				} else {
					this.removeModule('poll')
				}
			}
		}
	}
}
</script>
<style lang="stylus">
.c-sidebar-addons
	.bunt-checkbox
		margin-bottom: 8px
</style>
