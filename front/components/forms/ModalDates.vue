<template>
  <form action="" style="width: 1000px">
    <div class="modal-card" style="width: 900px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Добавление даты погрузки/разгрузки</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>
      <section class="dates-section">
        <div class="categories__calendar">
          <b-field label="Выберите дату погрузки и разгрузки">
            <b-datepicker
              placeholder="Кликните чтобы выбрать"
              v-model="dates"
              icon="calendar-today"
              append-to-body
              range>
            </b-datepicker>
          </b-field>
        </div>
      </section>
      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Добавить"
          :loading="loading"
          type="is-success"
          @click="sendDates"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
export default {
  name: "ModalDatesForm",
  props: ['confCalculate'],
  data() {
    return {
      dates: null,
      deliveryDateFromSeller: null,
      deliveryDateToBuyer: null,
      loading: false,
    }
  },
  methods: {
    async sendDates() {
      const data = {
        delivery_date_from_seller: this.dates[0].getDate() + '.' + (this.dates[0].getMonth() + 1) + '.' + this.dates[0].getFullYear(),
        delivery_date_to_buyer: this.dates[1].getDate() + '.' + (this.dates[1].getMonth() + 1) + '.' + this.dates[1].getFullYear()
      }
      this.loading = true
      const id = this.confCalculate.id
      await this.$store.dispatch('eggs/patchConfCalc', [data, id])
        .finally(() => this.loading = false, setTimeout(this.update, 1000))
      this.$emit('close')
      this.$router.push('/')
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

.categories {
  &__title {
    margin-bottom: 20px;
    font-size: 20px;
    font-weight: 500;
  }

  &__content {
    padding: 15px 30px;
  }

  &__row {
    display: grid;
    grid-template-columns: 100px 1fr 1fr;
    place-items: center;
    gap: 15px;
    padding-bottom: 15px;
    margin-bottom: 15px;
    border-bottom: 1px solid #EFF0F5;
  }

  &__dropdown {
    display: block;
    align-self: center;
    padding-bottom: 3px;
  }

  &__calendar {
    display: grid;
    grid-template-columns: 1fr;
    gap: 40px;
    margin-top: 20px;
    padding-bottom: 20px;
    border-bottom: 1px solid #EFF0F5;
  }
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
  &__button-wrapper{
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
}

.dates-section {
  background-color: #fff;
  padding: 3vh 3vw;
}

.my-input {
  height: 30px;
  border-radius: 5px;
  margin: 0.5vh 1vh;
  margin-top: 0;
  padding: 0 1vh;
  border-color: #f5f5f5;
}
</style>