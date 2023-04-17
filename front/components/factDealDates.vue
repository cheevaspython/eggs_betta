<template>
  <form action="" style="width: 900px">
    <div class="modal-card" style="width: 800px; height: 650px">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 700">{{ title }}</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')" />
      </header>

      <section class="modal-card-body is-fullwidth">
        <div class="date">
          <b-datepicker
            style="width: 560px;"
            v-model="date"
            inline>
          </b-datepicker>
        </div>
      </section>

      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Добавить доп. расход"
          type="is-success"
          @click="sendDate"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>
  
<script>
export default {
  name: 'factDealDates',
  props: ['deal'],
  data() {
    return {
      date: null
    }
  },
  methods: {
    async sendDate() {
      const dealId = this.deal.id
      const deal = {}
      if (this.deal.deal_status == 5) {
        deal.actual_loading_date = this.date.getDate() + '.' + (this.date.getMonth() + 1) + '.' + this.date.getFullYear()
      }
      else if (this.deal.deal_status == 8) {
        deal.actual_unloading_date = this.date.getDate() + '.' + (this.date.getMonth() + 1) + '.' + this.date.getFullYear()
      }
      await this.$store.dispatch('eggs/patchDeal', [deal, dealId])
      const updatedDeal =  await this.$store.dispatch('eggs/getModel', this.deal.id)
      await this.$store.dispatch('eggs/setCurrentDeal', updatedDeal)
      this.$emit('close')
    }
  },
  computed: {
    title() {
      if (this.deal.deal_status == 5) {
        return 'Дата фактической погрузки'
      }
      else if (this.deal.deal_status == 8) {
        return 'Дата фактической разгрузки'
      }
    }
  }
}
</script>

<style lang="scss" scoped>
form {
  font-family: 'Montserrat';
}

.date {
  display: flex;
  justify-content: center;
  margin-top: 15px;
}
</style>
  