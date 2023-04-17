<template>
	<div class="card box" v-if="expenseList" style="width: 40vw">
		<h4 class="title has-text-centered border">Доп. расход</h4>
    <ul>
      <li v-for="item of sortObject(JSON.parse(this.expenseList))">
        <div class="expense-card flexbox flexbox__column">
          <div class="flexbox__row flexbox__space-around">
            <div class="part-left">{{ item.owner_name }}</div>
            <div class="part-right">{{ item.date_time }}</div>
          </div>
          <div class="flexbox__row flexbox__space-around">
            <div class="part-left">Расход: {{ item.expense }}</div>
            <div class="part-right">{{ item.comment }}</div>
          </div>
        </div>
      </li>
    </ul>
	</div>
</template>
    
<script>
export default {
	name: "ExpenseInfo",
	props: ['expenseList'],
  methods: {
    sortObject(obj) {
      return Object.keys(obj).sort().reduce(function (result, key) {
        result[key] = obj[key]
        return result
      }, {});
    }
  }
}
</script>
    
<style lang="scss" scoped>
.expense-card {
  border: solid 2px #dddddd;
  border-radius: 5px;
  padding: 0px;
  background-color: #ebebeb;
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
  &__space-between {
    justify-content: space-between;
  }
  &__space-around {
    justify-content: space-around;
  }
}

ul {
  list-style-type: none;
  max-height: 85vh;
  overflow-y: scroll;
  margin: 0;
}

.part-left {
  width: 40%;
  height: 50%;
  text-align: center;
  border: solid 1px #ebebeb;
  border-radius: 5px;
  background-color: #fff;
  overflow-wrap: break-word;
}

.part-right {
  width: 60%;
  height: 50%;
  text-align: center;
  border: solid 1px #ebebeb;
  border-radius: 5px;
  background-color: #fff;
  overflow-wrap: break-word;
}

.card {
	width: 100%;
}

.border {
	height: 40px;
	padding-top: 7px;
	border: solid #f8f8f8 2px;
	border-radius: 5px;
	background-color: #f3f3f3;
}
</style>
    