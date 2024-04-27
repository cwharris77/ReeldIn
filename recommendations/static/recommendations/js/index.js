// if the user is starting a new recommendation, this message pops up
window.onload = function () {
  let from_where = document.referrer.split("/");
  if (!from_where.includes("recommendations")) {
    alert(
      `This is ReeldIn's main functionality - the recommendation feature!\n
As you walk through our questions, we'll query our movie pool for what matches your inputs.
Click the button in the top right labeled 'Generate Recommendation' when you're ready!
Note the bottom of the page's counter on how many possible movies remaining meet your criteria. If it ever drops below ten, we'll stop early.
Happy querying!`
    );
  }
};
