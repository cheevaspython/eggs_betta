<template>
  <div class="card box" v-if="traderData">
    <h4 class="title has-text-centered">{{ title || 'Карточка' }}</h4>
    <div class="card__row">Название: <span class="card__info">{{ data.name || '-' }}</span></div>
    <div class="card__row">Инн: <span class="card__info">{{ data.inn || '-' }}</span></div>
    <div class="card__row">Ген Директор: <span class="card__info">{{ data.generalManager || '-' }}</span></div>
    <div class="card__row">Телефон: <span class="card__info">{{ data.contactPhone || '-' }}</span></div>
    <div class="card__row">Email: <span class="card__info">{{ data.email || '-' }}</span></div>
    <div class="card__row">Адрес: <span class="card__info">{{ data.address || '-' }}</span></div>
    <div class="card__row">Способ Оплаты: <span class="card__info">{{ data.paymentType || '-' }}</span></div>
    <div class="card__row">Комментарий: <span class="card__info">{{ data.comment || '-' }}</span></div>
    <hr>
    <h5 class="title has-text-centered">Реквизиты компании:</h5>
    <div class="card__row">Название Банка: <span class="card__info">{{ data.bankDetails.name || '-' }}</span></div>
    <div class="card__row">Бик Банка: <span class="card__info">{{ data.bankDetails.bik || '-' }}</span></div>
    <div class="card__row">Кор. счет: <span class="card__info">{{ data.bankDetails.cor || '-' }}</span></div>
    <div class="card__row">Расчетный счет: <span class="card__info">{{ data.bankDetails.account || '-' }}</span></div>
    <div class="card__row">Юр. адрес: <span class="card__info">{{ data.bankDetails.address || '-' }}</span></div>
    <div class="card__button-wrapper">
      <b-button type="is-info" @click="makeOrder">Создать Заявку</b-button>
    </div>

  </div>
</template>

<script>
import ModalForm from "~/components/ModalForm";
export default {
  name: "Card",
  props: ['traderData'],
  data() {
    return {
      title: 'Карточка продавца',
      data: {
        name: '',
        inn: '',
        generalManager: '',
        contactPhone: '',
        email: '',
        address: '',
        paymentType: '',
        comment: '',
        bankDetails: {
          name: '',
          bik: '',
          cor: '',
          account: '',
          address: ''
        }

      }
    }
  },
  watch: {
    traderData() {
      this.filterData()
    }
  },
  methods: {
    filterData() {
      const {
        name,
        inn,
        general_manager,
        phone,
        email,
        legal_address,
        payment,
        comment,
        bank_name,
        bic_bank,
        cor_account,
        customers_account,
        warehouse_address,
        physical_address
      } = this.traderData
      this.data.name = name
      this.data.inn = inn
      this.data.generalManager = general_manager
      this.data.contactPhone = phone
      this.data.email = email
      this.data.address = physical_address
      this.data.paymentType = payment
      this.data.comment = comment
      this.data.bankDetails.name = bank_name
      this.data.bankDetails.bik = bic_bank
      this.data.bankDetails.cor = cor_account
      this.data.bankDetails.account = customers_account
      this.data.bankDetails.address = legal_address
    },

    makeOrder(){
      this.$buefy.modal.open({
        parent: this,
        component: ModalForm,
        hasModalCard: true,
        trapFocus: true,
        props:{
          trader: this.traderData
        }
      })
    }
  },

}
</script>

<style lang="scss" scoped>
.card {
  width: 100%;

  &__row {
    display: flex;
    justify-content: space-between;
    margin-bottom: .5rem;
  }

  &__info {
    font-weight: 500;
    margin-left: 1rem;
  }
  &__button-wrapper{
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
}
</style>
