<template>
  <div class="card box" v-if="traderData" style="width: 40vw">
    <h4 class="title has-text-centered border">{{ 'Карточка продавца' }}</h4>
    <div class="card__row">Название: <span class="card__info">{{ traderData.name || '-' }}</span></div>
    <div class="card__row">Инн: <span class="card__info">{{ traderData.inn || '-' }}</span></div>
    <div class="card__row">Контактное лицо: <span class="card__info">{{ traderData.contact_person || '-' }}</span></div>
    <div class="card__row">Телефон: <span class="card__info">{{ traderData.phone || '-' }}</span></div>
    <div class="card__row">Email: <span class="card__info">{{ traderData.email || '-' }}</span></div>
    <div class="card__row">Способ Оплаты: <span class="card__info">{{ getStrPayType || 'Не указан' }}</span></div>
    <div class="card__row">Комментарий: <span class="card__info">{{ traderData.comment || '-' }}</span></div>
    <div class="card__row">Менеджер: <span class="card__info">{{ traderData.manager_details || '-' }}</span></div>
    
    <div v-if="traderData.current_requisites">
      <h4 class="title has-text-centered border">Реквизиты компании</h4>
      <div class="card__row">Ген Директор: <span class="card__info">{{ traderData.current_requisites.general_manager || '-' }}</span></div>
      <div class="card__row">Название Банка: <span class="card__info">{{ traderData.current_requisites.bank_name || '-' }}</span></div>
      <div class="card__row">Бик Банка: <span class="card__info">{{ traderData.current_requisites.bic_bank || '-' }}</span></div>
      <div class="card__row">Кор. счет: <span class="card__info">{{ traderData.current_requisites.cor_account || '-' }}</span></div>
      <div class="card__row">Расчетный счет: <span class="card__info">{{ traderData.current_requisites.customers_pay_account || '-' }}</span></div>
      <div class="card__row">Юр. адрес: <span class="card__info">{{ traderData.current_requisites.legal_address || '-' }}</span></div>
      <div class="card__row">Факт. адрес: <span class="card__info">{{ traderData.current_requisites.physical_address || '-' }}</span></div>
    </div>
  </div>
</template>
  
<script>
export default {
  name: "SellerInfo",
  props: ['traderData'],
  computed: {
    getStrPayType() {
      switch(this.traderData.paymentType) {
        case 1:
          return 'С НДС'
        case 2:
          return 'Без НДС'
        case 3:
          return 'Наличка'
      }
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
  