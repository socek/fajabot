<script setup>
  import { onMounted, onUnmounted, ref } from 'vue'
  import axios from 'axios'

  let lastTime = null;
  let cycleReference = null;
  const propme = ref(null);

  const handleEvent = async (element) => {
    console.log(element)
    propme.value = true;
    setTimeout(() => {
      propme.value = null;
    }, 2000)
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
      ELO
      <div v-if="propme">
        EVENT! {{propme}}
      </div>
    </div>
  </header>
</template>
