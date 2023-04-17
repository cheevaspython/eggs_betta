<template>
<form action="" style="width: 1100px">
    <div class="modal-card" style="width: 1000px; height: 50vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Замечание по {{ title }} №{{ task.id }}</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')" />
      </header>

      <section class="modal-card-body is-fullwidth">
        <div>
          <div>Замечание</div>
          <b-field>
            <b-input v-model="note" type="textarea" maxlength="500"></b-input>
          </b-field>
        </div>
      </section>

      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Отправить"
          type="is-success"
          @click="sendNote"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>
    
<script>
export default {
	name: "note",
	props: ['task', 'title'],
  data() {
    return {
      note: null,
    }
  },
  methods: {
    async sendNote() {
      if (this.title == 'Просчету') {
        await this.$store.dispatch('eggs/patchCalc', [{note_calc: this.note}, this.task.id, false])
          .finally(() => setTimeout(this.update, 1000))
        this.$emit('close')
      }
      else if (this.title == 'Подтвержденному просчету') {
        await this.$store.dispatch('eggs/patchConfCalc', [{note_conf_calc: this.note}, this.task.id, false])
          .finally(() => setTimeout(this.update, 1000))
        this.$emit('close')
      }
    },
    update() {
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
    },
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
</style>
    