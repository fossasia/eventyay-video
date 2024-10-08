<template lang="pug">
prompt.c-av-device-prompt(@close="$emit('close')")
	.content
		h2 {{ $t('AVDevicePrompt:headline:label') }}
		bunt-select(v-if="videoInputs.length > 0", v-model="videoInput", @input="refreshVideo", :options="videoInputs", option-label="label", option-value="value", icon="camera", name="videoInput")
		.video-wrapper
			video(ref="video", playsinline, autoplay, muted="muted")
		bunt-select(v-if="audioInputs.length > 0", v-model="audioInput", :options="audioInputs", option-label="label", option-value="value", icon="microphone", name="audioInput")
		bunt-select(v-if="audioOutputs.length > 0", v-model="audioOutput", :options="audioOutputs", option-label="label", option-value="value", icon="volume-high", name="audioOutput")
		bunt-checkbox(v-model="videoOutput", name="videoOutput") {{ $t(`AVDevicePrompt:videoout:label`) }}
		bunt-button.btn-action(@click="save") {{ $t(`AVDevicePrompt:apply:label`) }}

</template>
<script>
import Prompt from 'components/Prompt'

export default {
	components: {Prompt},
	props: {},
	data() {
		return {
			videoInput: localStorage.videoInput || '',
			audioInput: localStorage.audioInput || '',
			audioOutput: localStorage.audioOutput || '',
			videoOutput: localStorage.videoOutput !== 'false',
			videoInputs: [],
			audioInputs: [],
			audioOutputs: [],
			stream: null,
		}
	},
	computed: {},
	mounted() {
		navigator.mediaDevices.enumerateDevices().then(this.gotDevices).catch((e) => {
			console.warn(e)
			alert('Could not access camera or microphone, is another program on your machine using it right now?')
			// todo
		})
	},
	methods: {
		gotDevices(deviceInfos) {
			this.videoInputs = [
				{
					value: '',
					label: this.$t('AVDevicePrompt:default:label')
				}
			]
			this.audioInputs = [
				{
					value: '',
					label: this.$t('AVDevicePrompt:default:label')
				}
			]
			this.audioOutputs = [
				{
					value: '',
					label: this.$t('AVDevicePrompt:default:label')
				}
			]
			for (const deviceInfo of deviceInfos) {
				if (deviceInfo.kind === 'audioinput') {
					this.audioInputs.push({
						label: deviceInfo.label || `microphone ${this.audioInputs.length + 1}`,
						value: deviceInfo.deviceId,
					})
				} else if (deviceInfo.kind === 'audiooutput') {
					this.audioOutputs.push({
						label: deviceInfo.label || `speaker ${this.audioOutputs.length + 1}`,
						value: deviceInfo.deviceId,
					})
				} else if (deviceInfo.kind === 'videoinput') {
					this.videoInputs.push({
						label: deviceInfo.label || `camera ${this.videoInputs.length + 1}`,
						value: deviceInfo.deviceId,
					})
				} else {
					console.log('Some other kind of source/device: ', deviceInfo)
				}
			}
			this.refreshVideo()
		},
		refreshVideo() {
			console.log('refresh')
			if (this.stream) {
				this.stream.getTracks().forEach(track => {
					track.stop()
				})
			}
			const constraints = {
				audio: {},
				video: {deviceId: this.videoInput ? {exact: this.videoInput} : undefined},
			}
			navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
				this.stream = stream
				this.$refs.video.srcObject = stream
				this.$refs.video.muted = 'muted'
				// Refresh button list in case labels have become available
				return navigator.mediaDevices.enumerateDevices()
			}).catch((e) => {
				// todo
				// possibly "overconstrained" (camera doesn't exist)
			})
		},
		save() {
			localStorage.videoInput = this.videoInput || ''
			localStorage.audioInput = this.audioInput || ''
			localStorage.audioOutput = this.audioOutput || ''
			localStorage.videoOutput = this.videoOutput
			this.$emit('close')
		},
	},
}
</script>
<style lang="stylus">
	.c-av-device-prompt
		.content
			display: flex
			flex-direction: column
			padding: 16px
			justify-items: center

			h2
				margin: 0
				text-align: center
			.video-wrapper
				background: black
				width: 320px
				max-width: 90vw
				margin: auto
				height: 180px
				position: relative
				overflow: hidden
				border-radius: 5px
			video
				max-height: 100%
				max-width: 100%
				height: 100%
				object-fit: contain
				width: 100%
			.btn-action
				themed-button-primary(size: large)
</style>
