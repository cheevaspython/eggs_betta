<template>
  <form action="" style="width: 1000px">
    <div class="modal-card" style="width: 900px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Добавление логиста</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>
      <section class="log-section">
        <div class="card__row">
          <b-dropdown :triggers="['hover']" aria-role="list" style="margin-bottom: 8px">
            <template #trigger>
              <b-button
                v-model="currentLogic"  
                label="Выберите логиста"
                type="is-success is-light"
                icon-right="menu-down"
                rounded />
            </template>
            <b-dropdown-item aria-role="listitem" v-for="logic in logists" :key="logic.name" @click="selectLogist(logic)">
              <strong>{{ logic.name }}</strong>
            </b-dropdown-item>
          </b-dropdown>
          <span class="card__info" v-if="currentLogic">
            {{currentLogic.name}}
          </span>
        </div>
        <b-button type="is-success is-light" rounded label="Создать логиста" @click="createNewLogic"/>
      </section>
      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Добавить"
          :loading="loading"
          type="is-success"
          @click="sendLogic"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
import ModalCreateLogicForm from '@/components/forms/ModalCreateLogicForm'
export default {
  name: "ModalLogicForm",
  props: ['confCalculate'],
  data() {
    return {
      currentLogic: null,
      deliveryCost: 0,
      loading: false,
    }
  },
  methods: {
    createNewLogic() {
      this.$buefy.modal.open({
        parent: this,
        component: ModalCreateLogicForm,
        hasModalCard: true,
        trapFocus: true
      })
    },
    selectLogist(logic) {
      this.currentLogic = logic
    },
    async sendLogic() {
      const data = {
        current_logic: this.currentLogic.id,
      }
      this.loading = true
      const id = this.confCalculate.id
      const updatedConfCalc = await this.$store.dispatch('eggs/patchConfCalc', [data, id, true])
        .finally(() => this.loading = false, setTimeout(this.update, 1000))
      // const updatedConfCalc = await this.$store.dispatch('eggs/getModel', id)
      await this.$store.dispatch('eggs/setCurrentConfCalculate', updatedConfCalc)
      this.$emit('close')
    },
    update() {
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
    }
  },
  mounted() {
    this.$store.dispatch('ca/getLogists')
  },
  computed: {
    logists() {
      return this.$store.state.ca.logists
    }
  }
}
</script>

<style lang="scss" scoped>
form {
  font-family: 'Montserrat';
}

.card {
  width: 100%;

  &__row {
    display: flex;
    font-size: 16px;
    justify-content: space-between;
    margin-bottom: .5rem;
    border-bottom: solid #f5f5f5 2px;
  }
  &__info {
    overflow-wrap: break-word;
    font-size: 16px;
    max-width: 500px;
    font-weight: 500;
    margin-left: 1rem;
  }
}

.log-section {
  background-color: #fff;
  padding: 3vh 3vw;
}
</style>