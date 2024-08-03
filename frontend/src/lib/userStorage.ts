// This file is used to store the user id in the local storage of the browser.
// fairly simple, it has two functions, getUserId and setUserId.
// interest in saving time
export const getUserId = () => {
    if (typeof window !== 'undefined') {
        const userId = localStorage.getItem('userId');
        return userId ? parseInt(userId, 10) : null;
    }
    return null;
};

export const setUserId = (userId: string) => {
    if (typeof window !== 'undefined') {
        localStorage.setItem('userId', userId);
    }
};
