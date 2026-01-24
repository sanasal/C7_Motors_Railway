function updateCalculator() {
    let price = Number(document.getElementById("car_price").value);
    let downPercent = Number(document.getElementById("down_percent").value);
    let interest = Number(document.getElementById("interest_rate").value);
    let years = Number(document.querySelector(".period-btn.active").dataset.value);

    // Keep downpayment in sync with percent
    let downpayment = price * (downPercent / 100);
    document.getElementById("downpayment").value = downpayment.toFixed(0);

    // Keep sliders in sync
    document.getElementById("price_slider").value = price;
    document.getElementById("down_slider").value = downPercent;
    document.getElementById("interest_slider").value = interest;

    let loanAmount = price - downpayment;
    let totalInterest = loanAmount * (interest / 100) * years;
    let totalWithInterest = loanAmount + totalInterest;
    let monthly = totalWithInterest / (years * 12);

    // Update UI
    document.getElementById("monthly_payment").innerText = "AED " + monthly.toFixed(0);
    document.getElementById("s_car_price").innerText = "AED " + price.toLocaleString();
    document.getElementById("s_downpayment").innerText = 
        "AED " + downpayment.toLocaleString() + " / " + downPercent + "%";
    document.getElementById("s_loan_amount").innerText = "AED " + loanAmount.toLocaleString();
    document.getElementById("s_period").innerText = years + " Years";
    document.getElementById("s_interest").innerText = "AED " + totalInterest.toFixed(0);
}

// Get elements
const price_slider = document.getElementById("price_slider");
const car_price = document.getElementById("car_price");
const down_slider = document.getElementById("down_slider");
const down_percent = document.getElementById("down_percent");
const downpayment = document.getElementById("downpayment");
const interest_slider = document.getElementById("interest_slider");
const interest_rate = document.getElementById("interest_rate");

// Sliders sync
price_slider.oninput = () => {
    car_price.value = price_slider.value;
    updateCalculator();
};
down_slider.oninput = () => {
    down_percent.value = down_slider.value;
    updateCalculator();
};
interest_slider.oninput = () => {
    interest_rate.value = interest_slider.value;
    updateCalculator();
};

// Input fields sync
car_price.oninput = () => updateCalculator();
down_percent.oninput = () => updateCalculator();
interest_rate.oninput = () => updateCalculator();

// Make downpayment editable too
downpayment.oninput = () => {
    const price = Number(car_price.value);
    const dp = Number(downpayment.value);
    down_percent.value = ((dp / price) * 100).toFixed(2);
    updateCalculator();
};

// Period buttons
document.querySelectorAll(".period-btn").forEach(btn => {
    btn.onclick = () => {
        document.querySelectorAll(".period-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        updateCalculator();
    };
});

// Run on load
updateCalculator();