<template>
  <form action="" style="width: 1250px">
    <div class="modal-card" style="width: 1100px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Доп. расход {{ title }}</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')" />
      </header>

      <section class="modal-card-body is-fullwidth flexbox__column">
        <div class="flexbox__column">
          <div class="card__row">Текущий доп. расход:
            <span class="card__info">{{ task.expense_total }} ₽</span>
          </div>
          
          <div class="flexbox__row" style="width: 1060px">
            <div class="flexbox__row flexbox__space-between input-border">
              <div style="margin-left: 10px; margin-top: 8px;">Доп. расход ₽</div>
              <b-field style="width: 60%">
                <b-input placeholder="Введите сумму" rounded v-model="additionalExpense"></b-input>
              </b-field>
            </div>
          </div>
  
          <div class="card__row">
            Комментарий к доп.расходу:
          </div>
          <b-field>
            <b-input v-model="additionalExpenseDetail" type="textarea" maxlength="255"></b-input>
          </b-field>
        </div>
      </section>

      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Добавить доп. расход"
          type="is-success"
          @click="addExpense"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
export default {
  name: "addExpenseForm",
  props: ['task', 'title'],
  data() {
    return {
      additionalExpense: null,
      additionalExpenseDetail: '',
    }
  },
  methods: {
    getStrMonth(month) {
      switch (month) {
        case 0:
          return 'января'
        case 1:
          return 'февраля'
        case 2:
          return 'марта'
        case 3:
          return 'апреля'
        case 4:
          return 'мая'
        case 5:
          return 'июня'
        case 6:
          return 'июля'
        case 7:
          return 'августа'
        case 8:
          return 'сентября'
        case 9:
          return 'октября'
        case 10:
          return 'ноября'
        case 11:
          return 'декабря'
      }
    },
    getStrDay(dateStr) {
      const date = Date.parse(dateStr)
      const currentDate = new Date(date)
      return currentDate.getDate() + ' ' + this.getStrMonth(currentDate.getMonth()) + ' ' + currentDate.getFullYear()
    },
    update() {
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
    },
    async addExpense() {
      const expense = {
        tmp_json: {},
      }
      const owner = localStorage.getItem('userId')
      const fullName = localStorage.getItem('fullName')
      const today = new Date()
      let minute = `${today.getMinutes()}`
      let hour = `${today.getHours()}`
      minute = (minute.length == 1) ? '0' + minute : minute
      hour = (hour.length == 1) ? '0' + hour : hour
      const date = today.getDate() + ' ' + this.getStrMonth(today.getMonth()) + ' ' + today.getFullYear() + ' ' + hour + ":" + minute

      if (this.additionalExpense) {
        expense.tmp_json = {
          owner_id: owner,
          owner_name: fullName,
          expense: this.additionalExpense,
          comment: this.additionalExpenseDetail,
          date_time: date
        }
        this.$store.dispatch('eggs/addExpense', [expense, this.task.additional_expense])
        if (this.task.status == 3) {
          const updatedDeal =  await this.$store.dispatch('eggs/getModel', this.task.id)
          await this.$store.dispatch('eggs/setCurrentDeal', updatedDeal)
        }
        else if (this.task.status == 2) {
          const updatedConfCalc = await this.$store.dispatch('eggs/getModel', this.task.id)
          await this.$store.dispatch('eggs/setCurrentConfCalculate', updatedConfCalc)
        }
      }
      this.$emit('close')
    }
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
  &__space-between{
    justify-content: space-between;
  }
}

.card {
  width: 100%;
  
  &__row {
    display: flex;
    justify-content: space-between;
    margin-bottom: .5rem;
    border-bottom: solid #f5f5f5 2px;
  }
  &__info {
    overflow-wrap: break-word;
    max-width: 500px;
    font-weight: 500;
    margin-left: 1rem;
  }
}

.input-border {
  border: solid 2px #ebebeb;
  border-radius: 20px;
  width: 1060px;
  height: 44px;
  margin-bottom: 5px;
}
</style>
