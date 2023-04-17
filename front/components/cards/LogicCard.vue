<template>
  <div class="card box" v-if="traderData" style="width: 40vw">
    <h4 class="title has-text-centered border">{{ title || 'Карточка' }}</h4>
    <div class="card__row">Название: <span class="card__info">{{ data.name || '-' }}</span></div>
    <div class="card__row">Инн: <span class="card__info">{{ data.inn || '-' }}</span></div>
    <div class="card__row">Контактное лицо: <span class="card__info">{{ data.contact_person || '-' }}</span></div>
    <div class="card__row">Телефон: <span class="card__info">{{ data.contactPhone || '-' }}</span></div>
    <div class="card__row">Email: <span class="card__info">{{ data.email || '-' }}</span></div>
    <div class="card__row">Способ Оплаты: <span class="card__info">{{ data.paymentType || 'Не указан' }}</span></div>
    <div class="card__row">Комментарий: <span class="card__info">{{ data.comment || '-' }}</span></div>
    
    <div v-if="data.requisitesDetails">
      <h4 class="title has-text-centered border">Реквизиты компании</h4>
      <div class="card__row">Ген Директор: <span class="card__info">{{ data.requisitesDetails.general_manager || '-' }}</span></div>
      <div class="card__row">Название Банка: <span class="card__info">{{ data.requisitesDetails.bank_name || '-' }}</span></div>
      <div class="card__row">Бик Банка: <span class="card__info">{{ data.requisitesDetails.bic_bank || '-' }}</span></div>
      <div class="card__row">Кор. счет: <span class="card__info">{{ data.requisitesDetails.cor_account || '-' }}</span></div>
      <div class="card__row">Расчетный счет: <span class="card__info">{{ data.requisitesDetails.customers_pay_account || '-' }}</span></div>
      <div class="card__row">Юр. адрес: <span class="card__info">{{ data.requisitesDetails.legal_address || '-' }}</span></div>
      <div class="card__row">Факт. адрес: <span class="card__info">{{ data.requisitesDetails.physical_address || '-' }}</span></div>
    </div>
  </div>
</template>
  
<script>
export default {
  name: "LogicCard",
  props: ['traderData'],
  data() {
    return {
      title: 'Карточка логиста',
      data: {
        name: '',
        inn: '',
        contact_person: '',
        contactPhone: '',
        email: '',
        address: '',
        paymentType: '',
        comment: '',
        requisitesDetails: {}
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
        current_seller,
        name,
        inn,
        general_manager,
        phone,
        contact_person,
        email,
        pay_type,
        comment,
        current_requisites
      } = this.traderData
      this.data.current_seller = current_seller
      this.data.name = name
      this.data.inn = inn
      this.data.generalManager = general_manager
      this.data.contact_person = contact_person
      this.data.contactPhone = phone
      this.data.email = email
      this.data.paymentType = pay_type
      this.data.comment = comment
      this.data.requisitesDetails = current_requisites
    }
  }
}
</script>
  
<style lang="scss" scoped>
.card {
  width: 100%;
  background-color: #fff;

  &__row {
    display: flex;
    justify-content: space-between;
    margin-bottom: .5rem;
    border-bottom: solid #f5f5f5 2px;
  }

  &__info {
    overflow-wrap: break-word;
    max-width: 500px;
    font-weight: 1000;
    margin-left: 1rem;
  }
  &__button-wrapper{
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
}

.border {
  height: 40px;
  padding-top: 7px;
  border: solid #f8f8f8 2px;
  border-radius: 20px;
  background-color: #f3f3f3;
  margin-bottom: 10px;
}
</style>
  