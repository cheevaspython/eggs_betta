<template>
  <div class="card box" style="width: 40vw" v-if="appBuyer">
    <div class="card__row trader-info">Покупатель: 
      <span class="card__info">{{ appBuyer.buyer_card_detail.name }}</span>
    </div>
    <div class="card__row trader-info">ИНН: 
      <span class="card__info">{{ appBuyer.buyer_card_detail.inn }}</span>
    </div>
    
    <div class="has-text-centered border">Продукция</div>
    
    <fullTable :app="appBuyer" style="width: 100%"/>     

    <div class="has-text-centered border">Информация</div>
    <div class="card__row" v-show="appBuyer.postponement_pay">Отсрочка оплаты: 
      <span class="card__info">{{ postponementPayToStr || '-' }}</span>
    </div>
    <div class="card__row">Адрес разгрузки: 
      <span class="card__info">{{ appBuyer.unloading_address || '-' }}</span>
    </div>
    <div class="card__row">Окно поставки: 
      <span class="card__info">{{ `от ${getStrDay(appBuyer.delivery_window_from)} до ${getStrDay(appBuyer.delivery_window_until)}` }}</span>
    </div>
    <div class="card__row" v-show="appBuyer.comment">Комментарий: 
      <span class="card__info">{{ appBuyer.comment }}</span>
    </div>
    <div class="card__row">Автор: 
      <span class="card__info">{{ appBuyer.owner_detail.first_name + ' ' + appBuyer.owner_detail.last_name || '-' }}</span>
    </div>
  </div>
</template>
  
<script>
export default {
  name: 'appBuyer',
  props: ['appBuyer'],
  data() {
    return {
      currentBuyer: null,
      showBuyerCard: false
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
      if (this.appBuyer.postponement_pay == 1) {
        day = 'день'
      }
      else if (this.appBuyer.postponement_pay == 2 || this.appBuyer.postponement_pay == 3 || this.appBuyer.postponement_pay == 4) {
        day = 'дня'
      }
      else {
        day = 'дней'
      }
      const postponement = `${this.appBuyer.postponement_pay} ${day}`
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
  