<template>
  <section class="section">
    <div>
      <h3>ID просчета: {{currentTask.id}}</h3>
        <pre v-if="currentTask" id="json">{{currentTask}}</pre>
    </div>
  </section>
</template>

<script>

export default {
  name: 'IndexPage',
  data(){
    return {
    }
  },
  computed: {
    currentTask() {
      return this.$store.state.eggs.currentTask
    }
  },
  components: {
  },
  mounted() {
    console.log('####### state ', this.$store.state)
  }
}
</script>
