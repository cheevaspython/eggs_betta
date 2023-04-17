<template>
    <form action="" style="width: 1000px; height: 95vh;">
      <div class="modal-card" style="width: 900px">
        <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
          <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Оплата депозитом по Форме 1</p>
          <button
            type="button"
            class="delete"
            @click="$emit('close')"/>
        </header>
  
        <section class="modal-card-body is-fullwidth">
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin: 0 10px" v-show="buyer">Покупатель</div>
            <div style="margin: 0 10px" v-show="!buyer">Продавец</div>
            <b-field>
              <span class="card__info" style="margin-right: 10px;">{{ `${name} / ${inn}` }}</span>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border" v-if="buyer">
            <div style="margin: 0 10px">Лимит</div>
            <b-field>
              <span class="card__info" style="margin-right: 10px;">{{ payLimit }} ₽</span>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin: 0 10px">Текущая задолженность</div>
            <b-field>
              <span class="card__info" style="margin-right: 10px;">{{ debt }} ₽</span>
            </b-field>
          </div>
          <div class="flexbox__row flexbox__space-between input-border">
            <div style="margin: 0 10px">Депозит</div>
            <b-field>
              <span class="card__info" style="margin-right: 10px;">{{ tail.total_amount }} ₽</span>
            </b-field>
          </div>
  
          <div class="flexbox flexbox__center" style="margin-top: 20px; text-align: center; color: orange;">Выберите сделки для оплаты</div>
  
          <ul class="deal-list">
            <li class="deal flexbox flexbox__column" 
              v-for="deal in debtDeals" :key="deal.id" 
              v-bind:style="{'border-color': getBorderColor(deal)}">
              <div class="flexbox flexbox__space-between hover" style="width: 100%; cursor: pointer; margin-bottom: 3px" @click="payment(deal)">
                <div>Сделка №{{ deal.id }}, задолженность</div>
                <div>{{ deal.current_deal_buyer_debt }} ₽</div>
              </div>
              <div v-show="dealsOnPayment.includes(deal)" class="flexbox flexbox__row flexbox__space-between input-border">
                <div style="margin-left: 10px;">Сумма платежа ₽</div>
                <b-field class="my-small-input">
                  <b-input placeholder="Введите сумму" v-model="onDealPayment[deal.id].quantity" rounded></b-input>
                </b-field>
              </div>
            </li>
          </ul>
        </section>
  
        <footer class="modal-card-foot is-justify-content-flex-end">
          <b-button
            label="Подтвердить оплату"
            :loading="loading"
            type="is-success"
            @click="entryPayment"/>
          <b-button
            label="Закрыть"
            @click="$emit('close')"/>
        </footer>
      </div>
    </form>
  </template>
  
  <script>
  export default {
    name: "ModalDepositForm",
    props: ['trader', 'buyer', 'form', 'uuid', 'tail'],
    data() {
      return {
        name: this.trader.name,
        inn: this.trader.inn,
        payLimit: this.trader.pay_limit,
        debt: this.trader.balance_form_one < 0 ? Math.abs(this.trader.balance_form_one) : 0 ,
        loading: false,
        debtDeals: null,
        onDealPayment: {},
        dealsOnPayment: [],
      }
    },
    created() {
      if (this.trader.debt_deals) {
        this.debtDeals = this.trader.debt_deals.filter(el => el.cash == false)
        for (let deal of this.debtDeals) {
          this.onDealPayment[deal.id] = {
            id: deal.id,
            current_deal_buyer_debt: deal.current_deal_buyer_debt,
            documents: deal.documents,
            doc_type: null,
            date: null,
            quantity: null
          }
        }
      }
    },
    methods: {
      payment(deal) {
        if (this.dealsOnPayment[0] == deal) {
          this.dealsOnPayment = []
        }
        else {
          this.dealsOnPayment = [deal]
        }
      },
      getBorderColor(deal) {
        if (this.dealsOnPayment.includes(deal)) {
          return '#c2c2c2'
        }
        else {
          return '#ebebeb'
        }
      },
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
      async entryPayment() {
        if (this.dealsOnPayment.length == 0) {
          return alert('Выберите сделку для оплаты')
        }
        const dealId = this.dealsOnPayment[0].id
        if (!this.onDealPayment[dealId].quantity) {
          return alert('Вы не указали сумму платежа')
        }
        if (!confirm('Внести платеж?')) {
          return
        }

        const tmp_json_for_multi_pay_order = {
          date: this.tail.date,
          number: parseInt(this.tail.number),
          inn: parseInt(this.tail.inn),
          total_amount: parseFloat(this.tail.total_amount),
          other_pays: []
        }
        if (this.form) {
          tmp_json_for_multi_pay_order.tail_form_one = 0
          tmp_json_for_multi_pay_order.tail_form_two = null
        }
        else {
          tmp_json_for_multi_pay_order.tail_form_one = null
          tmp_json_for_multi_pay_order.tail_form_two = 0
        }
        let deals = []
        let summaryPayment = 0
        for (let deal of this.dealsOnPayment) {
          const currentDeal = {}
          currentDeal.pay_quantity = parseFloat(this.onDealPayment[deal.id].quantity)
          currentDeal.documents_id = parseInt(this.onDealPayment[deal.id].documents)
          currentDeal.deal = parseInt(deal.id)
          summaryPayment += parseFloat(this.onDealPayment[deal.id].quantity)
          deals = deals.concat(currentDeal)
        }
        const remainder = parseFloat(this.tail.total_amount) - parseFloat(summaryPayment)
        if (remainder < 0) {
          return alert('Сумма платежей по сделкам превышает общую сумму депозита')
        }
        const depositPay = {}
        if (remainder > 0) {
          const conf = confirm(`Остались нерасходованные средства по депозиту: ${remainder} ₽\nДанная сумма останется на депозите\nПродолжить?`)
          if (!conf) {
            return
          }
          if (this.form) {
            depositPay.tmp_key_form_dict = {
              form_one: this.uuid
            }
            tmp_json_for_multi_pay_order.tail_form_one = parseFloat(remainder)
          }
          else {
            depositPay.tmp_key_form_dict = {
              form_two: this.uuid
            }
            tmp_json_for_multi_pay_order.tail_form_two = parseFloat(remainder)
          }
          if (deals.length > 0) {
            tmp_json_for_multi_pay_order.other_pays = deals
          }
        }
        depositPay.tmp_json_for_multi_pay_order = tmp_json_for_multi_pay_order
        const pay = await this.$store.dispatch('ca/payTails', [depositPay, this.trader.tails_id])

        await this.$store.dispatch('ca/getBuyersDebt')
        await this.$store.dispatch('ca/getSellersDebt')
        this.$emit('close')
        if (!pay) return alert('Ошибка при проведении платежа')
      }
    },
  }
  </script>
  
  <style lang="scss" scoped>
  form {
    font-family: 'Montserrat';
  }
  
  ul {
    list-style-type: none;
    max-height: 450px;
    overflow-y: scroll;
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
  
  .input-border {
    border: solid 2px #ebebeb;
    border-radius: 20px;
    width: 100%;
    height: 40px;
    margin-bottom: 5px;
    align-items: center;
  }
  
  .my-b-input {
    width: 75%;
  }
  
  .my-small-input {
    width: 50%;
  }
  
  .deal-list {
    border: solid 2px #ebebeb;
    border-radius: 20px;
    padding: 5px;
    margin-bottom: 5px;
  }
  
  .deal {
    border: solid 2px #ebebeb;
    border-radius: 5px;
    margin-bottom: 2px;
  }
  
  .hover {
    border-radius: 5px;
    padding: 0 10px;
  
    &:hover {
      background-color: #f5f5f5;
    }
  }
  
  .upload {
    height: 30px;
    width: 100%;
    border: solid 2px #ebebeb;
    border-radius: 20px;
    padding-left: 15px;
    margin-bottom: 5px;
    cursor: pointer;
  
    &:hover {
      background-color: #f5f5f5;
    }
  }
  
  .hint {
    color: orange;
    margin-left: 10px;
  }
  
  .rdy-to-download {
    margin-left: 10px;
    color: green;
  }
  
  .calendar-border {
    border: solid 2px #ebebeb;
    border-radius: 20px;
    width: 100%;
    padding: 5px;
    margin-bottom: 5px;
  }
  
  .changeDates {
    display: flex;
    color: white;
    justify-content: center;
    font-size: 18px;
    border-radius: 15px;
    background-color: #823bf570;
  }
  </style>
  