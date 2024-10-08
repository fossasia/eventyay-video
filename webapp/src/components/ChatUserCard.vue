<template lang="pug">
.c-chat-user-card
	.ui-background-blocker(v-if="!userAction", @click="$emit('close')")
	.user-card(v-if="!userAction", :class="{deleted: user.deleted}", ref="card", @mousedown="showMoreActions=false")
		scrollbars(y)
			avatar(:user="user", :size="128")
			.name
				.online-status(v-if="!user.deleted", :class="onlineStatus ? 'online' : (onlineStatus === false ? 'offline' : 'unknown')", v-tooltip="onlineStatus ? $t('UserAction:state.online:tooltip') : (onlineStatus === false ? $t('UserAction:state.offline:tooltip') : '')")
				| {{ getUserName(user) }}
				.ui-badge(v-for="badge in user.badges") {{ badge }}
			ProfileFields(:user="user")
			.state {{ userStates.join(', ') }}
			.actions(v-if="user.id !== ownUser.id && user.id && !user.deleted")
				bunt-button.btn-dm(v-if="hasPermission('world:chat.direct')", @click="openDM") {{ $t('UserAction:action.dm:label') }}
				bunt-button.btn-call(v-if="hasPermission('world:chat.direct')", @click="startCall") {{ $t('UserAction:action.call:label') }}
				menu-dropdown(v-model="showMoreActions", :blockBackground="false", @mousedown.native.stop="")
					template(v-slot:button="{toggle}")
						bunt-icon-button(@click="toggle") dots-vertical
					template(v-slot:menu)
						.unblock(v-if="isBlocked", @click="userAction = 'unblock'") {{ $t('UserAction:action.unblock:label') }}
						.block(v-else, @click="userAction = 'block'") {{ $t('UserAction:action.block:label') }}
						template(v-if="hasPermission('room:chat.moderate') && user.id !== ownUser.id")
							.divider {{ $t('UserAction:moderator-actions:title') }}
							.reactivate(v-if="user.moderation_state", @click="userAction = 'reactivate'")
								| {{ user.moderation_state === 'banned' ? $t('UserAction:action.unban:label') : $t('UserAction:action.unsilence:label') }}
							.ban(v-if="user.moderation_state !== 'banned'", @click="userAction = 'ban'") {{ $t('UserAction:action.ban:label') }}
							.silence(v-if="!user.moderation_state", @click="userAction = 'silence'") {{ $t('UserAction:action.silence:label') }}
	user-action-prompt(v-if="userAction", :action="userAction", :user="user", @close="$emit('close')")
</template>
<script>
// TODO
// - i18n
import { mapState, mapGetters } from 'vuex'
import api from 'lib/api'
import { getUserName } from 'lib/profile'
import Avatar from 'components/Avatar'
import MenuDropdown from 'components/MenuDropdown'
import UserActionPrompt from 'components/UserActionPrompt'
import ProfileFields from 'components/profile/ProfileFields'

export default {
	components: { Avatar, MenuDropdown, UserActionPrompt, ProfileFields },
	props: {
		user: Object,
	},
	data() {
		return {
			blockedUsers: null,
			showMoreActions: false,
			userAction: null,
			moderationError: null,
			onlineStatus: null
		}
	},
	computed: {
		...mapState({
			ownUser: 'user',
			world: 'world'
		}),
		...mapGetters(['hasPermission']),
		isBlocked() {
			if (!this.blockedUsers) return
			return this.blockedUsers.some(user => user.id === this.user.id)
		},
		userStates() {
			const states = []
			if (this.isBlocked) {
				states.push('blocked')
			}
			if (this.user.moderation_state) {
				states.push(this.user.moderation_state)
			}
			return states
		}
	},
	async created() {
		this.onlineStatus = (await api.call('user.online_status', {ids: [this.user.id]}))[this.user.id]
		this.blockedUsers = (await api.call('user.list.blocked')).users
	},
	methods: {
		getUserName,
		async openDM() {
			// TODO loading indicator
			await this.$store.dispatch('chat/openDirectMessage', {users: [this.user]})
		},
		async startCall() {
			const channel = await this.$store.dispatch('chat/openDirectMessage', {users: [this.user]})
			await this.$store.dispatch('chat/startCall', {channel})
		}
	}
}
</script>
<style lang="stylus">
.c-chat-user-card
	.user-card
		card()
		z-index: 801
		display: flex
		flex-direction: column
		align-items: center
		min-width: 196px
		max-width: 380px
		min-height: 0
		max-height: 400px
		.scroll-content
			padding: 8px
		&.deleted
			.name
				color: $clr-disabled-text-light
				text-decoration: line-through
		.name
			font-size: 24px
			font-weight: 600
			margin-top: 8px
		.fields
			display: flex
			flex-direction: column
			align-self: stretch
			margin: 0 8px
			.field
				display: flex
				flex-direction: column
				margin: 4px
				.label
					color: $clr-secondary-text-light
					font-weight: 500
					font-size: 12px
				.value
					margin: 2px 0 0 8px
		.state
			height: 16px
		.online-status
			display: inline-block
			margin-right: 8px
			&::before
				content: ''
				display: inline-block
				background-color: $clr-grey-400
				width: 8px
				height: 8px
				border-radius: 50px
				vertical-align: middle
			&.online::before
				background-color: $clr-success
		.actions
			margin-top: 16px
			display: flex
			align-self: stretch
			justify-content: flex-end
			.bunt-button
				button-style(style: clear)
			.bunt-icon-button
				icon-button-style(style: clear)
			.c-menu-dropdown .menu
				.delete-message
					color: $clr-danger
					&:hover
						background-color: $clr-danger
						color: $clr-primary-text-dark
				.reactivate, .unblock
					color: $clr-success
					&:hover
						background-color: $clr-success
						color: $clr-primary-text-dark
				.ban, .block
					color: $clr-danger
					&:hover
						background-color: $clr-danger
						color: $clr-primary-text-dark
				.silence
					color: $clr-deep-orange
					&:hover
						background-color: $clr-deep-orange
						color: $clr-primary-text-dark
</style>
