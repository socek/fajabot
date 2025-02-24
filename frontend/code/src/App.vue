<script setup>
  import { onMounted, onUnmounted, ref } from 'vue'
  import axios from 'redaxios'

  const sounds = {
    "Alpissd1": "Alpissd1.mp3",
    "Alpissd1": "Alpissd1.mp3",
    "Fist": "Fist.mp3",
    "Hdead": "Hdead.mp3",
    "Ocapture": "Ocapture.mp3",
    "Pig": "Pig.mp3",
    "Sword1": "Sword1.mp3",
    "Sword2": "Sword2.mp3",
    "Sword3": "Sword3.mp3",
    "Wzpissd1": "Wzpissd1.mp3",
  }

  let lastTime = null;
  let cycleReference = null;

  const handleEvent = async (element) => {
    console.log(element);
  }

  const fetchData = async () => {
    const res = await axios.get(
      '/api/obsalerts',
      {
          params: {"time": lastTime}
      }
    )
    res.data.elements.forEach(async (element) => {
      handleEvent(element)
    })
    lastTime = res.data.time
  }

  onMounted(async () => {
    const res = await axios('/api/obsalerts')
    lastTime = res.data.time
    cycleReference = setInterval(fetchData, 1000)
  })

  onUnmounted(async () => {
    clearInterval(cycleReference)
  })
</script>

<template>
  <header>
    <div class="wrapper">
      <audio v-for="(filename, key) in sounds" :src="'/sounds/' + filename" :id="key" />
    </div>
  </header>
</template>
