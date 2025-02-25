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

  const events = {
    chatgra: async (element) => {
      await document.querySelector('#Ocapture').play()
    },
    profile: async (element) => {
      await document.querySelector('#Pig').play()
    },
    quest: async (element) => {
    },
    fight: async (element) => {
      const isActive = element.payload.active
      const fightResult = element.payload.fight_log.stages[1].result

      const sounds = {
        "profile_is_hit": "Sword2",
        "profile_is_not_hit": "Fist",
        "enemy_is_hit": "Sword3",
        "enemy_is_not_hit": "Fist",
        "draw": "Sword1",
      }

      if(isActive == false) {
        document.querySelector('#Sword1').play()
      } else {
        document.querySelector('#' + sounds[fightResult]).play()
      }
    },
    strimmore: async (element) => {
      await document.querySelector('#Wzpissd1').play()
    },
  }

  const handleEvent = async (element) => {
    const handler = events[element.payload.event];
    if(handler) {
      await handler(element);
    } else {
      console.log("Event handler not found", element);
    }
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
