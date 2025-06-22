
const states = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", 
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", 
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", 
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", 
    "Uttar Pradesh", "Uttarakhand", "West Bengal"
];


const districts = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati", "Kakinada"],
    "Arunachal Pradesh": ["Itanagar", "Tawang", "Ziro", "Bomdila", "Namsai"],
    "Assam": ["Guwahati", "Dibrugarh", "Jorhat", "Tezpur", "Silchar"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Munger"],
    "Chhattisgarh": ["Raipur", "Bilaspur", "Durg", "Korba", "Raigarh"],
    "Goa": ["Panaji", "Vasco da Gama", "Margao", "Mapusa", "Panjim"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"],
    "Haryana": ["Chandigarh", "Gurugram", "Faridabad", "Karnal", "Ambala"],
    "Himachal Pradesh": ["Shimla", "Manali", "Kullu", "Mandi", "Dharamshala"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Hazaribagh", "Giridih"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubballi", "Mangalore", "Belagavi"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Kottayam", "Alappuzha"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Thane"],
    "Manipur": ["Imphal", "Thoubal", "Churachandpur", "Bishnupur", "Senapati"],
    "Meghalaya": ["Shillong", "Tura", "Jowai", "Nongstoin", "Williamnagar"],
    "Mizoram": ["Aizawl", "Lunglei", "Champhai", "Kolasib", "Mamit"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Wokha", "Mon"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Berhampur", "Rourkela", "Sambalpur"],
    "Punjab": ["Amritsar", "Ludhiana", "Chandigarh", "Patiala", "Jalandhar"],
    "Rajasthan": ["Jaipur", "Udaipur", "Jodhpur", "Kota", "Ajmer"],
    "Sikkim": ["Gangtok", "Mangan", "Namchi", "Rangpo", "Jorethang"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
    "Telangana": ["Hyderabad", "Warangal", "Khammam", "Nizamabad", "Karimnagar"],
    "Tripura": ["Agartala", "Udaipur", "Dharmanagar", "Amarpur", "Belonia"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Allahabad"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Nainital", "Rishikesh", "Haldwani"],
    "West Bengal": ["Kolkata", "Howrah", "Siliguri", "Durgapur", "Asansol"]
};

// Example crops per state (you can expand these with real agricultural data)
const cropSuggestions = {
    "Andhra Pradesh": [
        { crop: "Rice", yield: 2200 }, // Yield per acre in kg
        { crop: "Groundnut", yield: 800 },
        { crop: "Cotton", yield: 1000 }
    ],
    
    "Assam": [
        { crop: "Tea", yield: 4000 },
        { crop: "Rice", yield: 2500 },
        { crop: "Mustard", yield: 1200 }
    ],
    
    // Add crops for other states as needed
};
sessionStorage.setItem("crops", JSON.stringify([
  { crop: "Wheat", yield: 1200 },
  { crop: "Rice", yield: 1500 },
  { crop: "Maize", yield: 1000 }
]));
// Simulating rainfall prediction (you would typically use an API to get actual data)
const rainfallPrediction = {
    "Visakhapatnam": "Heavy rain expected",
    "Vijayawada": "Light rain expected",
    "Guwahati": "Moderate rain expected",
    // Add more districts with predictions
};

// Function to populate the state dropdown dynamically
function populateStates() {
    const stateList = document.getElementById("state-list");
    states.forEach(state => {
        const option = document.createElement("option");
        option.value = state;
        stateList.appendChild(option);
    });
}

// Function to update the district list based on the selected state
function updateDistricts() {
    const stateInput = document.getElementById("state");
    const districtInput = document.getElementById("district");
    const state = stateInput.value;

    // Clear the district list before adding new districts
    const districtList = document.getElementById("district-list");
    districtList.innerHTML = "";

    // If a valid state is selected, populate the district list
    if (districts[state]) {
        districtInput.disabled = false;
        districts[state].forEach(district => {
            const option = document.createElement("option");
            option.value = district;
            districtList.appendChild(option);
        });
    } else {
        districtInput.disabled = true;
    }
}

document.getElementById("summary-district").textContent = sessionStorage.getItem("district");
document.getElementById("summary-temp").textContent = sessionStorage.getItem("temperature");
document.getElementById("summary-humidity").textContent = sessionStorage.getItem("humidity");
document.getElementById("summary-rain").textContent = sessionStorage.getItem("rainPrediction");


// Function to simulate rainfall prediction based on selected district
function getRainfallPrediction(district) {
    return rainfallPrediction[district] || "No rainfall data available for this district";
}

// Function to get crop suggestions based on selected state
function getCropSuggestions(state) {
    return cropSuggestions[state] || [];
}




function getClimateData() {
    const state = document.getElementById("state").value;
    const district = document.getElementById("district").value;

    if (!state || !district) {
        alert("Please select both a state and a district.");
        return;
    }

    console.log(`Fetching data for State: ${state}, District: ${district}`);

    fetch(`http://127.0.0.1:5000/get_climate_data?state=${state}&district=${district}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert("Error fetching climate data. Please try again.");
                return;
            }

            // Update session storage
            sessionStorage.setItem("state", data.state);
            sessionStorage.setItem("district", data.district);
            sessionStorage.setItem("temperature", data.temperature);
            sessionStorage.setItem("humidity", data.humidity);
            sessionStorage.setItem("rainPrediction", data.rainPrediction);
            sessionStorage.setItem("crops", JSON.stringify(data.crops));
            sessionStorage.setItem("monthlyWeather", JSON.stringify(data.monthlyWeather));
            sessionStorage.setItem("crops", JSON.stringify([
  { crop: "Wheat", yield: 2200 },
  { crop: "Rice", yield: 1800 },
  { crop: "Maize", yield: 2000 }
]));


            // Update the UI
            document.getElementById("summary-state").textContent = data.state;
            document.getElementById("summary-district").textContent = data.district;
            document.getElementById("summary-temp").textContent = data.temperature;
            document.getElementById("summary-humidity").textContent = data.humidity;
            document.getElementById("summary-rain").textContent = data.rainPrediction;

            // Optionally, display crop suggestions
            const crops = data.crops;
            const cropList = document.getElementById("crop-list");
            cropList.innerHTML = ""; // Clear previous crops
            crops.forEach(crop => {
                const li = document.createElement("li");
                li.textContent = `${crop.crop} - Estimated Yield: ${crop.yield} kg/acre`;
                cropList.appendChild(li);
            });

            // Optionally, render a chart for monthly weather data
            renderMonthlyWeatherChart(data.monthlyWeather);

            // Redirect to dataPage.html if needed
            // window.location.href = "dataPage.html";
        })
        .catch(error => {
            console.error('Error fetching climate data:', error);
            alert('Failed to fetch data. Please try again later.');
        });
}

// Function to render a chart for monthly weather data
function renderMonthlyWeatherChart(monthlyWeather) {
    const ctx = document.getElementById("rainfall-chart").getContext("2d");
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: monthlyWeather.months,
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: monthlyWeather
                }
            ]
        }
    }
)}