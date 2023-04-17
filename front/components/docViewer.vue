<template>
  <form action="" style="width: 1200px">
    <div class="modal-card" style="width: 1100px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">{{ doc[1] }}</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')" />
      </header>

      <section class="modal-card-body is-fullwidth">
        <vue-pdf-embed :source="doc[0]" />
      </section>

      <footer class="modal-card-foot is-justify-content-flex-end">
        <a :href="doc[0]" class="download-btn">Скачать</a>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>
  
<script>
import VuePdfEmbed from "vue-pdf-embed/dist/vue2-pdf-embed"
export default {
  name: 'documentsViewer',
  components: {
    VuePdfEmbed
  },
  props: ['doc']
}
</script>

<style lang="scss" scoped>
form {
  font-family: 'Montserrat';
}

.download-btn {
  border: solid 1px #d5d5d5;
  background-color: #48c78e;
  border-radius: 4px;
  color: white;
  font-weight: 700;
  height: 40px;
  width: 97px;
  text-align: center;
  padding: 6px;
  margin-right: 10px;
}
</style>
  