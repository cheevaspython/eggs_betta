<template>
	<form action="" style="width: 1000px">
    <div class="modal-card" style="width: 900px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Просмотр договора</p>
        <button
        type="button"
        class="delete"
        @click="$emit('close')"/>
      </header>
      <section class="modal-card-body is-fullwidth">
        <vue-pdf-embed :source="trader.url" />
      </section>
      <footer class="modal-card-foot is-justify-content-flex-end">
        <a :href="trader.url" class="download-btn">Скачать</a>
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
	name: "CAContract",
	props: ['trader'],
  components: {
    VuePdfEmbed
  }
}
</script>
    
<style lang="scss" scoped>
form {
  font-family: 'Montserrat';
}

.flexbox {
  display: flex;

  &__column {
    flex-direction: column;
    flex-flow: column;
  }
  &__row {
    flex-direction: row;
    flex-flow: row;
    display: inline-flex;
  }
  &__start {
    justify-content: flex-start;
  }
  &__center {
    justify-content: center;
  }
  &__end {
    justify-content: flex-end;
  }
  &__space-between {
    justify-content: space-between;
  }
  &__space-around {
    justify-content: space-around;
  }
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
    