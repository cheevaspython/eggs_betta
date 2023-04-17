<template>
  <form action="" style="width: 1000px; height: 95vh;">
    <div class="modal-card" style="width: 900px">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Внесение входящего платежа по Форме 1</p>
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

        <div style="text-align: center; color: orange;" v-show="!(universalPayment || paymentOrder)">Выберите тип платежки</div>

        <div class="flexbox__row flexbox__space-between input-border" v-show="!paymentOrder">
          <div style="margin-left: 10px;">Общая платежка</div>
          <b-checkbox :value="true"
            type="is-success"
            size="is-medium"
            v-model="universalPayment">
          </b-checkbox>
        </div>
        <div class="flexbox__row flexbox__space-between input-border" v-show="!universalPayment && debtDeals">
          <div style="margin-left: 10px;">Платежное поручение входящее</div>
          <b-checkbox :value="true"
            type="is-success"
            size="is-medium"
            v-model="paymentOrder">
          </b-checkbox>
        </div>

        <div class="upload" v-if="paymentOrder">
          <div>Платежное поручение входящее</div>
          <div v-show="payment_order_incoming" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!payment_order_incoming" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" id="statistic_payment_order_incoming" ref="statistic_payment_order_incoming" @change="previewPayOrderIncoming" />
        </div>
        <div class="upload" v-if="universalPayment">
          <div>Общая платежка</div>
          <div v-show="multi_pay_order" class="rdy-to-download">Файл готов к загрузке</div>
          <div v-show="!multi_pay_order" class="hint">Нажмите чтобы загрузить</div>
          <input style="padding-bottom: 10px; z-index: 100;" accept=".pdf" type="file" id="multi_pay_order" ref="multi_pay_order" @change="previewMultyPayOrderIncoming" />
        </div>
        <div v-if="multi_pay_order">
          <div class="flexbox flexbox__row flexbox__space-between calendar-border">
            <div class="flexbox__column">
              <div class="changeDates">Дата документа</div>
              <div class="flexbox__row flexbox__space-between" style="margin-top: 15px">
                <b-datepicker
                  style="width: 360px;"
                  v-model="docDate"
                  inline>
                </b-datepicker>
              </div>
            </div>
            <div class="flexbox__column" style="display: flex; padding-top: 50px;">
              <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; margin-bottom: 5px">
                <div style="margin-left: 10px;">Номер документа</div>
                <b-field class="my-small-input">
                  <b-input placeholder="Введите номер" v-model="docNumber" rounded></b-input>
                </b-field>
              </div>
              <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; margin-bottom: 5px">
                <div style="margin-left: 10px;">Сумма ₽</div>
                <b-field class="my-small-input">
                  <b-input placeholder="Введите сумму" v-model="encroachment" rounded></b-input>
                </b-field>
              </div>
            </div>
          </div>
        </div>

        <div v-show="docDate && docNumber && encroachment" class="flexbox flexbox__center" style="margin-top: 20px; text-align: center; color: orange;">Выберите сделки для оплаты</div>
        <div v-show="payment_order_incoming" class="flexbox flexbox__center" style="margin-top: 20px; text-align: center; color: orange;">Выберите сделку для оплаты</div>

        <ul class="deal-list" v-show="(docDate && docNumber && encroachment) || payment_order_incoming">
          <li class="deal flexbox flexbox__column" 
            v-for="deal in debtDeals" :key="deal.id" 
            v-bind:style="{'border-color': getBorderColor(deal)}">
            <div class="flexbox flexbox__space-between hover" style="width: 100%; cursor: pointer; margin-bottom: 3px" @click="payment(deal)">
              <div>Сделка №{{ deal.id }}, задолженность</div>
              <div>{{ deal.current_deal_buyer_debt }} ₽</div>
            </div>
            <div v-show="dealsOnPayment.includes(deal)" style="margin-top: 10px"  v-if="!universalPayment">
              <div class="flexbox flexbox__row flexbox__space-between calendar-border">
                <div class="flexbox__column">
                  <div class="changeDates">Дата документа</div>
                  <div class="flexbox__row flexbox__space-between" style="margin-top: 15px">
                    <b-datepicker
                      style="width: 360px;"
                      v-model="onDealPayment[deal.id].date"
                      inline>
                    </b-datepicker>
                  </div>
                </div>
                <div class="flexbox__column" style="display: flex; padding-top: 50px;">
                  <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; margin-bottom: 5px">
                    <div style="margin-left: 10px;">Номер документа</div>
                    <b-field class="my-small-input">
                      <b-input placeholder="Введите номер" v-model="onDealPayment[deal.id].number" rounded></b-input>
                    </b-field>
                  </div>
                  <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; margin-bottom: 5px">
                    <div style="margin-left: 10px;">Сумма ₽</div>
                    <b-field class="my-small-input">
                      <b-input placeholder="Введите сумму" v-model="onDealPayment[deal.id].quantity" rounded></b-input>
                    </b-field>
                  </div>
                </div>
              </div>

            </div>
            <div v-else v-show="dealsOnPayment.includes(deal)" style="margin-top: 10px">
              <div class="flexbox__row flexbox__space-between input-border" style="width: 100%; margin-bottom: 5px">
                <div style="margin-left: 10px;">Сумма ₽</div>
                <b-field class="my-small-input">
                  <b-input placeholder="Введите сумму" v-model="onDealPayment[deal.id].quantity" rounded></b-input>
                </b-field>
              </div>
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
  name: "ModalPaymentForm",
  props: ['trader', 'buyer'],
  data() {
    return {
      name: this.trader.name,
      inn: this.trader.inn,
      payLimit: this.trader.pay_limit,
      debt: this.trader.balance_form_one < 0 ? Math.abs(this.trader.balance_form_one) : 0 ,
      docNumber: null,
      encroachment: null,
      comment: null,
      loading: false,
      universalPayment: false,
      paymentOrder: false,
      debtDeals: null,
      onDealPayment: {},
      dealsOnPayment: [],
      docDate: null,
      payment_order_incoming: null,
      multi_pay_order: null
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
  beforeUpdate() {
    if (!this.universalPayment && !this.paymentOrder) {
      this.dealsOnPayment = []
      this.multi_pay_order = null
      this.payment_order_incoming = null
    }
  },
  methods: {
    previewPayOrderIncoming() {
      this.payment_order_incoming = this.$refs.statistic_payment_order_incoming.files[0]
    },
    previewMultyPayOrderIncoming() {
      this.multi_pay_order = this.$refs.multi_pay_order.files[0]
    },
    payment(deal) {
      if (this.universalPayment) {
        if (!this.dealsOnPayment.includes(deal)) {
          this.dealsOnPayment.push(deal)
        }
        else {
          this.dealsOnPayment = this.dealsOnPayment.filter(el => el.id != deal.id)
        }
      }
      else {
        if (this.dealsOnPayment[0] == deal) {
          this.dealsOnPayment = []
        }
        else {
          this.dealsOnPayment = [deal]
        }
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
      if (this.universalPayment) {
        if (!this.multi_pay_order) {
          return alert('Вы не загрузили общую платежку')
        }
        if (!this.encroachment) {
          return alert('Вы не указали сумму общего платежа')
        }
        if (!this.docNumber) {
          return alert('Вы не указали номер документа')
        }
        if (!this.docDate) {
          return alert('Вы не указали дату документа')
        }
      }
      else {
        if (!this.payment_order_incoming) {
          return alert('Вы не загрузили входящee платежное поручение')
        }
        if (this.dealsOnPayment.length == 0) {
          return alert('Выберите сделку для оплаты')
        }
        const dealId = this.dealsOnPayment[0].id
        if (!this.onDealPayment[dealId].quantity) {
          return alert('Вы не указали сумму платежа')
        }
        if (!this.onDealPayment[dealId].number) {
          return alert('Вы не указали номер документа')
        }
        if (!this.onDealPayment[dealId].date) {
          return alert('Вы не указали дату документа')
        }
      }
      if (!confirm('Внести платеж?')) {
        return
      }

      if (this.universalPayment) {
        const formDataMulty = new FormData()
        formDataMulty.append('multi_pay_order', this.multi_pay_order)
        const date = this.docDate
        const docDate = date.getDate() + '.' + (date.getMonth() + 1) + '.' + date.getFullYear()
        const tmp_json_for_multi_pay_order = {
          date: docDate, 
          number: this.docNumber,
          inn: this.trader.inn,
          total_amount: this.encroachment,
          tail_form_one: 0,
          tail_form_two: null,
          other_pays: []
        }
        let deals = []
        let summaryPayment = 0
        for (let deal of this.dealsOnPayment) {
          const currentDeal = {}
          currentDeal.pay_quantity = this.onDealPayment[deal.id].quantity
          currentDeal.documents_id = this.onDealPayment[deal.id].documents
          currentDeal.deal = deal.id
          summaryPayment += parseFloat(this.onDealPayment[deal.id].quantity)
          deals = deals.concat(currentDeal)
        }
        const remainder = parseFloat(this.encroachment) - parseFloat(summaryPayment)
        if (remainder < 0) {
          return alert('Сумма платежей по сделкам превышает общую сумму платежа')
        }
        if (remainder > 0) {
          const conf = confirm(`Остались нерасходованные средства по платежке: ${remainder} ₽\nДанная сумма будет переведена на депозит\nПродолжить?`)
          if (!conf) {
            return
          }
          tmp_json_for_multi_pay_order.tail_form_one = remainder
          if (deals.length > 0) {
            tmp_json_for_multi_pay_order.other_pays = deals
          }
          formDataMulty.append('tmp_json_for_multi_pay_order', JSON.stringify(tmp_json_for_multi_pay_order))
        }
        
        this.encroachment = 0
        const payloadMulty = [formDataMulty, this.trader.documents_contract_id]
        await this.$store.dispatch('ca/documentsContract', payloadMulty)
      }
      else {
        const dealId = this.dealsOnPayment[0].id
        const formData = new FormData()
        const date = this.onDealPayment[dealId].date
        const docDate = date.getDate() + '.' + (date.getMonth() + 1) + '.' + date.getFullYear()
        formData.append('payment_order_incoming', this.payment_order_incoming)
        const data_for_tmp_json = {
          date: docDate,
          number: this.onDealPayment[dealId].number,
          pay_quantity: this.onDealPayment[dealId].quantity,
          inn: this.trader.inn,
          doc_type: 'payment_order_incoming'
        }
        formData.append('tmp_json', JSON.stringify(data_for_tmp_json))

        const docsPayload = [this.onDealPayment[dealId].documents, formData]
        const succes = await this.$store.dispatch('eggs/dealUpload', docsPayload)
        if (!succes) {
          return
        }
      }
      await this.$store.dispatch('ca/getBuyersDebt')
      this.$emit('close')
    },
    update() {
      this.$store.dispatch('ca/getBuyersDebt')
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
    },
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
