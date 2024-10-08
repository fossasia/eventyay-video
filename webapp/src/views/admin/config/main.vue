<template lang="pug">
.c-mainconfig
	.ui-page-header
		h1 Event Config
	scrollbars(y)
		bunt-progress-circular(size="huge", v-if="!config && !error")
		.error(v-if="error") We could not fetch the current configuration.
		.ui-form-body(v-if="config")
			h2 System details
			bunt-input(v-model="config.title", label="Title", name="title", :validation="$v.config.title")
			bunt-select(v-model="config.locale", label="Language", name="locale", :options="locales", option-value="code", option-label="nativeLabel")
			bunt-select(v-model="config.date_locale", label="Date locale", name="date_locale", :options="momentLocales")
			bunt-input(v-model="config.timezone", label="Time zone", name="timezone", :validation="$v.config.timezone")
			bunt-input(v-model="config.connection_limit", label="Connection limit", name="connection_limit", hint="Set to 0 to allow unlimited connections per user", :validation="$v.config.connection_limit")
			template(v-if="$features.enabled('conftool')")
				h2 Conftool
				bunt-input(v-model="config.conftool_url", label="Conftool REST API URL", name="conftool_url", :validation="$v.config.conftool_url")
				bunt-input(v-model="config.conftool_password", label="Conftool REST API Password", name="conftool_password")
			h2 Tracking and statistics
			bunt-checkbox(v-model="config.track_room_views", label="Track room views", name="track_room_views")
			bunt-checkbox(v-model="config.track_world_views", label="Track world views", name="track_world_views")
			bunt-checkbox(v-model="config.track_exhibitor_views", label="Track exhibitor views", name="track_exhibitor_views")
			h2 Settings for newly-created BBB rooms
			bunt-checkbox(v-model="config.bbb_defaults.record", label="Allow recording", name="record")
			bunt-checkbox(v-model="config.bbb_defaults.hide_presentation", label="Hide presentation when users join", name="hide_presentation")
			bunt-checkbox(v-model="config.bbb_defaults.waiting_room", label="Put new users in waiting room first (needs to be set before first join)", name="waiting_room")
			bunt-checkbox(v-model="config.bbb_defaults.auto_microphone", label="Auto-join users with microphone on (skip dialog asking how to join)", name="auto_microphone")
			bunt-checkbox(v-model="config.bbb_defaults.auto_camera", label="Auto-join users with camera on", name="auto_camera")
			bunt-checkbox(v-model="config.bbb_defaults.bbb_mute_on_start", label="Auto-mute users" name="bbb_mute_on_start")
			bunt-checkbox(v-model="config.bbb_defaults.bbb_disable_cam", label="Disable camera for non-moderators", name="bbb_disable_cam")
			bunt-checkbox(v-model="config.bbb_defaults.bbb_disable_chat", label="Disable public chat for non-moderators", name="bbb_disable_chat")
			h2 Settings for stages
			bunt-input-outline-container(label="hls.js config", :class="{error: $v.hlsConfig.$invalid}")
				textarea(slot-scope="{focus, blur}", @focus="focus", @blur="blur", v-model="hlsConfig")
			.json-error-message {{ $v.hlsConfig.$params.isJson.message }}
	.ui-form-actions
		bunt-button.btn-save(@click="save", :loading="saving", :error-message="error") Save
		.errors {{ validationErrors.join(', ') }}
</template>
<script>
import api from 'lib/api'
import { locales } from 'locales'
import { required, integer, isJson, url } from 'lib/validators'
import ValidationErrorsMixin from 'components/mixins/validation-errors'

const momentLocaleSet = [
	// do not use moment.locales() since moment lazy-loads locales and will only return "en" and the active locale
	'af', 'ar', 'ar-dz', 'ar-kw', 'ar-ly', 'ar-ma', 'ar-sa', 'ar-tn', 'az', 'be', 'bg', 'bm', 'bn', 'bo', 'br', 'bs',
	'ca', 'cs', 'cv', 'cy', 'da', 'de', 'de-at', 'de-ch', 'dv', 'el', 'en-au', 'en-ca', 'en-gb', 'en-ie', 'en-il',
	'en-in', 'en-nz', 'en-sg', 'eo', 'es', 'es-do', 'es-us', 'et', 'eu', 'fa', 'fi', 'fil', 'fo', 'fr', 'fr-ca', 'fr-ch',
	'fy', 'ga', 'gd', 'gl', 'gom-deva', 'gom-latn', 'gu', 'he', 'hi', 'hr', 'hu', 'hy-am', 'id', 'is', 'it', 'it-ch',
	'ja', 'jv', 'ka', 'kk', 'km', 'kn', 'ko', 'ku', 'ky', 'lb', 'lo', 'lt', 'lv', 'me', 'mi', 'mk', 'ml',
	'mn', 'mr', 'ms', 'ms-my', 'mt', 'my', 'nb', 'ne', 'nl', 'nl-be', 'nn', 'oc-lnc', 'pa-in', 'pl', 'pt', 'pt-br',
	'ro', 'ru', 'sd', 'se', 'si', 'sk', 'sl', 'sq', 'sr', 'sr-cyrl', 'ss', 'sv', 'sw', 'ta', 'te', 'tet',
	'tg', 'th', 'tk', 'tl-ph', 'tlh', 'tr', 'tzl', 'tzm', 'tzm-latn', 'ug-cn', 'uk', 'ur', 'uz', 'uz-latn', 'vi',
	'x-pseudo', 'yo', 'zh-cn', 'zh-hk', 'zh-mo', 'zh-tw',
]

export default {
	mixins: [ValidationErrorsMixin],
	data() {
		return {
			config: null,
			hlsConfig: '',
			saving: false,
			errors: [],
			error: null
		}
	},
	computed: {
		locales() {
			return locales
		},
		momentLocales() {
			return momentLocaleSet
		}
	},
	validations: {
		config: {
			title: {
				required: required('title is required')
			},
			timezone: {
				required: required('timezone is required')
			},
			connection_limit: {
				required: required('Connection Limit is required'),
				integer: integer('Connection limit must be a number')
			},
			conftool_url: {
				url: url('Conftool URL must be a URL'),
			},
		},
		hlsConfig: {
			isJson: isJson()
		}
	},
	async created() {
		// We don't use the global world object since it e.g. currently does not contain locale and timezone
		// TODO: Force reloading if world.updated is received from the server
		try {
			this.config = await api.call('world.config.get')
			this.hlsConfig = JSON.stringify(this.config.video_player?.['hls.js'] || undefined, null, 2)
		} catch (error) {
			this.error = error
			console.log(error)
		}
	},
	methods: {
		async save() {
			this.$v.$touch()
			if (this.$v.$invalid) return
			// TODO validate connection limit is a number
			this.saving = true
			const patch = {
				title: this.config.title,
				locale: this.config.locale,
				date_locale: this.config.date_locale,
				timezone: this.config.timezone,
				connection_limit: this.config.connection_limit,
				bbb_defaults: this.config.bbb_defaults,
				track_exhibitor_views: this.config.track_exhibitor_views,
				track_room_views: this.config.track_room_views,
				track_world_views: this.config.track_world_views
			}
			if (this.$features.enabled('conftool')) {
				patch.conftool_url = this.config.conftool_url
				patch.conftool_password = this.config.conftool_password
			}
			if (this.hlsConfig) {
				patch.video_player = {
					'hls.js': JSON.parse(this.hlsConfig)
				}
			} else {
				patch.video_player = null
			}
			await api.call('world.config.patch', patch)
			this.saving = false
			// TODO error handling
		},
	}
}
</script>
<style lang="stylus">
.c-mainconfig
	flex: auto
	display: flex
	flex-direction: column
	.bunt-input-outline-container
		margin-top: 16px
		&.error
			label
				color: $clr-danger
			.outline
				stroke: $clr-danger
				stroke-width: 2px
		textarea
			background-color: transparent
			border: none
			outline: none
			resize: vertical
			min-height: 120px
			padding: 0 8px
	.json-error-message
		color: $clr-danger
		margin: 4px
</style>
