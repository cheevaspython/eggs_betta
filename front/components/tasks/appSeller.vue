<template>
  <div class="card box" style="width: 40vw" v-if="appSeller">
    <div class="card__row trader-info">Продавец: 
      <span class="card__info">{{ appSeller.seller_card_detail.name }}</span>
    </div>
    <div class="card__row trader-info">ИНН: 
      <span class="card__info">{{ appSeller.seller_card_detail.inn }}</span>
    </div>
    
    <div class="has-text-centered border">Продукция</div>

    <fullTable :app="appSeller" style="width: 100%"/>

    <div class="has-text-centered border">Информация</div>
    <div class="flexbox__row flexbox__space-between" style="width: 100%">
        <div class="app-type app-type__import" v-show="appSeller.import_application">Импорт</div>
        <div class="app-type app-type__pre-payment" v-show="appSeller.pre_payment_application">Предоплата</div>
        <div class="app-type app-type__post-payment" v-show="!appSeller.pre_payment_application">Постоплата</div>
      </div>
    <div class="card__row" v-show="appSeller.postponement_pay">Отсрочка оплаты: 
      <span class="card__info">{{ postponementPayToStr || '-' }}</span>
    </div>
    <div class="card__row">Адрес погрузки: 
      <span class="card__info">{{ appSeller.loading_address || '-' }}</span>
    </div>
    <div class="card__row">Окно поставки: 
      <span class="card__info">{{ `от ${getStrDay(appSeller.delivery_window_from)} до ${getStrDay(appSeller.delivery_window_until)}` || '-' }}</span>
    </div>
    <div class="card__row" v-show="appSeller.comment">Комментарий: 
      <span class="card__info">{{ appSeller.comment || '-' }}</span>
    </div>
    <div class="card__row">Автор: 
      <span class="card__info">{{ appSeller.owner_detail.first_name + ' ' + appSeller.owner_detail.last_name || '-' }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'appSeller',
  props: ['appSeller'],
  data() {
    return {

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
  },
  computed: {
    postponementPayToStr() {
      let day
      if (this.appSeller.postponement_pay == 1) {
        day = 'день'
      }
      else if (this.appSeller.postponement_pay == 2 || this.appSeller.postponement_pay == 3 || this.appSeller.postponement_pay == 4) {
        day = 'дня'
      }
      else {
        day = 'дней'
      }
      const postponement = `${this.appSeller.postponement_pay} ${day}`
      return postponement
    }
  }
}
</script>

<style lang="scss" scoped>
.card {
  margin: 0;

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
  &__button-wrapper{
    margin-top: 20px;
    display: flex;
    justify-content: center;
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

.app-type {
  font-size: 14px;
  width: 100%;
  text-align: center;
  padding: 0;
  margin-bottom: 0.2vh;
  border: solid 1px #ebebeb;
  border-radius: 20px;

  &__import {
    background-color: #c411dc3f;
  }
  &__pre-payment {
    background-color: #a9680d4f;
  }
  &__post-payment {
    background-color: #9e9e9e45;
  }
}

.border {
  height: 28px;
  color: #00000095;
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 0.5vh;
  border: solid #f8f8f8 2px;
  border-radius: 5px;
  background-color: #f5f5f5;
}
</style>
