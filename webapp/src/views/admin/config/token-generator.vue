<template lang="pug">
.c-tokengenerator
	.ui-page-header
		h1 Token Generator
	scrollbars(y).ui-form-body
		bunt-input(v-model="number", label="Number", name="number", :validation="$v.number")
		bunt-input(v-model="days", label="Days", name="days", :validation="$v.days")
		bunt-input(label="Traits (comma-separated)", @input="set_traits($event)", name="t"
								:value="traits ? traits.join(', ') : ''")
		bunt-button.btn-generate(@click="save", :loading="saving") Generate
		bunt-input-outline-container(label="Result")
			textarea(slot-scope="{focus, blur}", @focus="focus", @blur="blur", v-model="result")
</template>
<script>
import api from 'lib/api'
import { DEFAULT_COLORS, DEFAULT_LOGO } from 'theme'
import { required, integer } from 'vuelidate/lib/validators'

export default {
	data() {
		return {
			traits: [],
			number: 1,
			days: 90,
			result: '',
			saving: false,
		}
	},
	validations: {
		number: {
			integer,
			required
		},
		days: {
			integer,
			required
		}
	},
	async created() {
		// TODO: Force reloading if world.updated is received from the server
		try {
			this.config = await api.call('world.config.get')

			// Enforce some defaults
			this.config.theme = {logo: {}, colors: {}, streamOfflineImage: null, textOverwrites: {}, ...this.config.theme}
			this.config.theme.colors = {...DEFAULT_COLORS, ...this.config.theme.colors}
			this.config.theme.logo = {...DEFAULT_LOGO, ...this.config.theme.logo}
		} catch (error) {
			this.error = error
			console.log(error)
		}
	},
	methods: {
		set_traits(t) {
			this.traits = t.split(',').map((i) => i.trim())
		},
		async save() {
			this.$v.$touch()
			if (this.$v.$invalid) return

			this.saving = true
			const r = await api.call('world.tokens.generate', {
				number: parseInt(this.number),
				days: parseInt(this.days),
				traits: this.traits
			})
			this.saving = false

			this.result = r.results.map((t) => `${location.protocol}//${location.host}/login/${t}`).join('\n')
			// TODO error handling
		},
	}
}
</script>
<style lang="stylus">
.c-tokengenerator
	flex: auto
	display: flex
	flex-direction: column
	.btn-generate
		margin-bottom: 32px
		themed-button-primary(size: large)
	.bunt-input-outline-container
		textarea
			background-color: transparent
			border: none
			outline: none
			resize: vertical
			min-height: 250px
			padding: 0 8px
</style>
