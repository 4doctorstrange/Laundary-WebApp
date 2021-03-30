const blah = document.getElementById('rform').children;
console.log(blah);

for (var i = 1; i<7; i++) {
    console.log(blah.item(i));
    var l1 = blah.item(i).children;
    
    l1.item(0).className += 'block text-gray-700 text-sm font-bold mb-2 ml-3';
    l1.item(1).className += 'bg-gray-200 rounded w-full text-gray-700 focus:outline-none border-b-4 border-gray-300 focus:border-purple-600 transition duration-500 px-3 pb-3';
    console.log(l1.item(1));
}